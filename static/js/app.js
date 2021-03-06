// fork getUserMedia for multiple browser versions, for the future
// when more browsers support MediaRecorder

navigator.getUserMedia = ( navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia);

// set up basic variables for app

var microphone = document.querySelector('.microphone');
var record = document.querySelector('.record');
var stop = document.querySelector('.stop');
var soundClips = document.querySelector('.sound-clips');
var canvas = document.querySelector('.visualizer');
var microphone_state = 'record';
// visualiser setup - create web audio api context and canvas

var audioCtx = new (window.AudioContext || webkitAudioContext)();
var canvasCtx = canvas.getContext("2d");

//main block for doing the audio recording

if (navigator.getUserMedia) {
    console.log('getUserMedia supported.');
    navigator.getUserMedia (
        // constraints - only audio needed for this app
        {
            audio: true
        },

        // Success callback
        function(stream) {
            var mediaRecorder = new MediaRecorder(stream);
            var chunks = [];
            visualize(stream);

            microphone.onclick = function() {
                if (microphone_state == 'record')
                {
                    mediaRecorder.start();
                    $('.record.microphone').addClass('stop').removeClass('record')
                    microphone_state = 'stop';
                    console.log(mediaRecorder.state);
                    console.log("recorder started");
                    //record.style.background = "red";
                    //record.style.color = "black";
                }else{
                    mediaRecorder.stop();
                    $('.stop.microphone').addClass('record').removeClass('stop')
                    microphone_state = 'record';
                    console.log(mediaRecorder.state);
                    console.log("recorder stopped");
                    //record.style.background = "";
                    //record.style.color = "";
                }
            }


            mediaRecorder.ondataavailable = function(e) {
                chunks.push(e.data);
            }

            mediaRecorder.onstop = function(e) {
                console.log("recorder stopped");

                var clipName = prompt('Enter a name for your sound clip');

                var clipContainer = document.createElement('article');
                var clipLabel = document.createElement('p');
                var audio = document.createElement('audio');
                var deleteButton = document.createElement('button');

                clipContainer.classList.add('clip');
                audio.setAttribute('controls', '');
                deleteButton.innerHTML = "Delete";
                clipLabel.innerHTML = clipName;

                clipContainer.appendChild(audio);
                clipContainer.appendChild(clipLabel);
                clipContainer.appendChild(deleteButton);
                soundClips.appendChild(clipContainer);

                var blob = new Blob(chunks, { 'type' : 'audio/wav; codecs=opus' });

                var fd = new FormData();
                fd.append('data', blob);
                $.ajax({
                    type: 'POST',
                    url: 'app/parse_audio_file',
                    data: fd,
                    processData: false,
                    contentType: false,
                    success: function(returned_data){
                        console.log(returned_data);
                    }
                });

                var audioURL = window.URL.createObjectURL(blob);
                audio.src = audioURL;

                deleteButton.onclick = function(e) {
                    var evtTgt = e.target;
                    evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
                }
            }
        },

        // Error callback
        function(err) {
            console.log('The following gUM error occured: ' + err);
        }
    );
} else {
    console.log('getUserMedia not supported on your browser!');
}

function visualize(stream) {
    var source = audioCtx.createMediaStreamSource(stream);

    var analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    var bufferLength = analyser.frequencyBinCount;
    var dataArray = new Uint8Array(bufferLength);

    source.connect(analyser);
    //analyser.connect(audioCtx.destination);

    WIDTH = canvas.width
    HEIGHT = canvas.height;

    draw()

    function draw() {

        requestAnimationFrame(draw);

        analyser.getByteTimeDomainData(dataArray);

        canvasCtx.fillStyle = 'rgb(200, 200, 200)';
        canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

        canvasCtx.beginPath();

        var sliceWidth = WIDTH * 1.0 / bufferLength;
        var x = 0;


        for(var i = 0; i < bufferLength; i++) {

            var v = dataArray[i] / 128.0;
            var y = v * HEIGHT/2;

            if(i === 0) {
                canvasCtx.moveTo(x, y);
            } else {
                canvasCtx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        canvasCtx.lineTo(canvas.width, canvas.height/2);
        canvasCtx.stroke();

    }
}

// document.getElementsByClassName('phone')[0].addEventListener("click", myFunction);

function myFunction() {
    // var phone = $('.phone');
    // var checkmark = $('.check_mark');
    // phone.toggleClass('pulse');
    // setTimeout(function(){
    //         phone.toggleClass('pulse');
    //         phone.toggleClass('sms-group')
    //         checkmark.toggleClass('tick-group');
    //        // phone.toggleClass('sms-group');
    //         }, 4000);
}