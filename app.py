<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini TTS Generator</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f7f9fb;
        }
    </style>
</head>
<body class="p-4 sm:p-8 min-h-screen flex items-start justify-center">

    <div id="app" class="w-full max-w-xl bg-white p-6 sm:p-8 rounded-2xl shadow-2xl border border-gray-100 transition-all duration-300">
        <h1 class="text-3xl font-extrabold text-gray-900 mb-2 flex items-center">
            <svg class="w-7 h-7 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2m-7 7h3"></path></svg>
            Gemini TTS Generator
        </h1>
        <p class="text-gray-600 mb-6">Convert text into reliable, high-quality speech using the Gemini API. Multilingual support is auto-detected.</p>

        <!-- Text Input -->
        <label for="text-input" class="block text-sm font-medium text-gray-700 mb-2">Enter your text:</label>
        <textarea id="text-input" rows="5" maxlength="1000" class="w-full p-4 border border-gray-300 rounded-xl focus:ring-indigo-500 focus:border-indigo-500 shadow-sm transition duration-150 ease-in-out resize-none" placeholder="Type your phrase here in English, Hindi, Spanish, etc. (max 1000 characters)..."></textarea>
        <p id="char-count" class="text-right text-xs text-gray-500 mt-1">0/1000</p>

        <!-- Voice Selection (Simplified) -->
        <div class="mt-4">
            <label for="voice-select" class="block text-sm font-medium text-gray-700 mb-2">Select Voice:</label>
            <select id="voice-select" class="w-full p-3 border border-gray-300 rounded-xl shadow-sm focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out">
                <!-- Using a strong, neutral voice that handles multiple languages well -->
                <option value="Kore" selected>Kore (Firm/Neutral)</option>
                <option value="Puck">Puck (Upbeat)</option>
                <option value="Charon">Charon (Informative)</option>
                <option value="Fenrir">Fenrir (Excitable)</option>
            </select>
        </div>


        <!-- Convert Button -->
        <button id="convert-button" class="mt-8 w-full bg-indigo-600 text-white py-3 rounded-xl font-semibold shadow-lg hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-500 focus:ring-opacity-50 transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
            <span id="button-text">🎙️ Generate Speech</span>
            <span id="spinner" class="hidden animate-spin h-5 w-5 border-4 border-white border-t-transparent rounded-full mr-2"></span>
        </button>

        <!-- Output Area -->
        <div id="output-area" class="mt-8 pt-4 border-t border-gray-200 hidden">
            <h2 class="text-xl font-bold text-gray-800 mb-3">Playback</h2>
            <div id="audio-player-container" class="p-4 bg-gray-50 rounded-lg shadow-inner">
                <audio id="audio-player" controls class="w-full">
                    Your browser does not support the audio element.
                </audio>
            </div>
            <div class="mt-4 flex justify-end">
                <button id="download-button" class="bg-green-500 text-white py-2 px-4 rounded-xl font-semibold shadow hover:bg-green-600 transition duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
                    ⬇️ Download WAV
                </button>
            </div>
        </div>

        <!-- Message Area -->
        <div id="message-box" class="mt-4 p-4 rounded-xl hidden text-sm font-medium"></div>

    </div>

    <script>
        // Global variables provided by the environment
        const apiKey = "";
        const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=${apiKey}`;

        // Utility functions for PCM audio handling (REQUIRED for Gemini TTS playback)
        
        /**
         * Converts a base64 string to an ArrayBuffer.
         */
        function base64ToArrayBuffer(base64) {
            const binary_string = window.atob(base64);
            const len = binary_string.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            // PCM data is 16-bit signed integers, so we need Int16Array
            return bytes.buffer; 
        }

        /**
         * Converts signed 16-bit PCM audio data to a WAV Blob.
         * The sample rate (e.g., 24000) is parsed from the API response or set to a default.
         */
        function pcmToWav(pcm16Data, sampleRate) {
            const numChannels = 1;
            const bytesPerSample = 2; // 16-bit PCM

            const buffer = new ArrayBuffer(44 + pcm16Data.byteLength);
            const view = new DataView(buffer);

            // RIFF header
            writeString(view, 0, 'RIFF');
            view.setUint32(4, 36 + pcm16Data.byteLength, true); // ChunkSize
            writeString(view, 8, 'WAVE');

            // FMT sub-chunk
            writeString(view, 12, 'fmt ');
            view.setUint32(16, 16, true); // Subchunk1Size (16 for PCM)
            view.setUint16(20, 1, true); // AudioFormat (1 for PCM)
            view.setUint16(22, numChannels, true); // NumChannels
            view.setUint32(24, sampleRate, true); // SampleRate
            view.setUint32(28, sampleRate * numChannels * bytesPerSample, true); // ByteRate
            view.setUint16(32, numChannels * bytesPerSample, true); // BlockAlign
            view.setUint16(34, 16, true); // BitsPerSample

            // DATA sub-chunk
            writeString(view, 36, 'data');
            view.setUint32(40, pcm16Data.byteLength, true); // Subchunk2Size

            // Write PCM data
            const pcmView = new Int16Array(pcm16Data);
            let offset = 44;
            for (let i = 0; i < pcmView.length; i++) {
                view.setInt16(offset, pcmView[i], true);
                offset += bytesPerSample;
            }

            return new Blob([buffer], { type: 'audio/wav' });

            function writeString(view, offset, string) {
                for (let i = 0; i < string.length; i++) {
                    view.setUint8(offset + i, string.charCodeAt(i));
                }
            }
        }

        // --- DOM Elements and Event Listeners ---
        const textInput = document.getElementById('text-input');
        const charCount = document.getElementById('char-count');
        const voiceSelect = document.getElementById('voice-select');
        const convertButton = document.getElementById('convert-button');
        const buttonText = document.getElementById('button-text');
        const spinner = document.getElementById('spinner');
        const outputArea = document.getElementById('output-area');
        const audioPlayer = document.getElementById('audio-player');
        const downloadButton = document.getElementById('download-button');
        const messageBox = document.getElementById('message-box');

        let audioBlob = null; // Store the blob for download

        textInput.addEventListener('input', () => {
            charCount.textContent = `${textInput.value.length}/1000`;
        });

        convertButton.addEventListener('click', generateSpeech);

        function showMessage(type, message) {
            messageBox.textContent = message;
            messageBox.className = 'mt-4 p-4 rounded-xl text-sm font-medium';
            messageBox.classList.remove('hidden', 'bg-red-100', 'text-red-700', 'bg-green-100', 'text-green-700');
            
            if (type === 'error') {
                messageBox.classList.add('bg-red-100', 'text-red-700', 'shadow');
            } else if (type === 'success') {
                messageBox.classList.add('bg-green-100', 'text-green-700', 'shadow');
            } else {
                messageBox.classList.add('hidden'); // Hide if type is 'clear'
            }
        }

        function setGenerating(isGenerating) {
            textInput.disabled = isGenerating;
            voiceSelect.disabled = isGenerating;
            convertButton.disabled = isGenerating;
            outputArea.classList.add('hidden');
            
            if (isGenerating) {
                buttonText.innerHTML = 'Generating...';
                spinner.classList.remove('hidden');
                convertButton.classList.add('flex', 'items-center', 'justify-center');
                showMessage('clear');
            } else {
                buttonText.textContent = '🎙️ Generate Speech';
                spinner.classList.add('hidden');
                convertButton.classList.remove('flex', 'items-center', 'justify-center');
            }
        }

        async function generateSpeech() {
            const prompt = textInput.value.trim();
            const selectedVoice = voiceSelect.value;

            if (!prompt) {
                showMessage('error', 'Please enter text to generate speech.');
                return;
            }

            setGenerating(true);

            // Construct the payload for the Gemini TTS API
            const payload = {
                contents: [{
                    parts: [{ text: prompt }]
                }],
                generationConfig: {
                    responseModalities: ["AUDIO"],
                    speechConfig: {
                        voiceConfig: {
                            prebuiltVoiceConfig: { voiceName: selectedVoice }
                        }
                    }
                },
                model: "gemini-2.5-flash-preview-tts"
            };

            let response;
            try {
                // Exponential backoff retry logic
                const maxRetries = 3;
                let delay = 1000;
                
                for (let i = 0; i < maxRetries; i++) {
                    response = await fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (response.status === 429 && i < maxRetries - 1) {
                        // Handle rate limiting specifically for the fetch call
                        await new Promise(resolve => setTimeout(resolve, delay));
                        delay *= 2; // Exponential backoff
                        continue; // Retry
                    }

                    if (!response.ok) {
                        const errorBody = await response.json();
                        throw new Error(`API error: ${response.status} - ${errorBody.error?.message || response.statusText}`);
                    }
                    break; // Success
                }

                const result = await response.json();
                const part = result?.candidates?.[0]?.content?.parts?.[0];
                const audioData = part?.inlineData?.data;
                const mimeType = part?.inlineData?.mimeType;

                if (!audioData || !mimeType || !mimeType.startsWith("audio/L16")) {
                    throw new Error("Invalid audio response structure from API.");
                }

                // Extract sample rate from MIME type (e.g., audio/L16; rate=24000)
                const rateMatch = mimeType.match(/rate=(\d+)/);
                const sampleRate = rateMatch ? parseInt(rateMatch[1], 10) : 24000;

                // 1. Convert Base64 data to ArrayBuffer
                const pcmDataBuffer = base64ToArrayBuffer(audioData);
                
                // 2. Convert 16-bit PCM data to WAV Blob
                audioBlob = pcmToWav(pcmDataBuffer, sampleRate);

                // 3. Create a URL for the audio player
                const audioUrl = URL.createObjectURL(audioBlob);
                
                // 4. Update the UI
                audioPlayer.src = audioUrl;
                outputArea.classList.remove('hidden');
                showMessage('success', 'Speech generated successfully! Click play to listen.');

            } catch (error) {
                console.error("Gemini TTS Error:", error);
                showMessage('error', `Generation failed: ${error.message}. Please try again.`);
            } finally {
                setGenerating(false);
            }
        }

        downloadButton.addEventListener('click', () => {
            if (audioBlob) {
                // Create a temporary link element
                const url = URL.createObjectURL(audioBlob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `speech_${new Date().toISOString().substring(0, 10)}.wav`;
                document.body.appendChild(a);
                a.click();
                
                // Clean up
                URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                showMessage('error', 'No audio generated to download.');
            }
        });

        // Initialize character count on load
        charCount.textContent = `${textInput.value.length}/1000`;
    </script>

</body>
</html>
