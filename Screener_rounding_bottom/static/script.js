<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Screener</title>
    <style>
        #progressBarContainer {
            width: 100%;
            background-color: #e0e0e0;
        }
        #progressBar {
            width: 0%;
            height: 30px;
            background-color: #4caf50;
            text-align: center;
            color: white;
            line-height: 30px;
        }
    </style>
</head>
<body>
    <h1>Stock Screener</h1>
    
    <button onclick="startScreening()">Start Screening</button>

    <div id="progressBarContainer">
        <div id="progressBar">0%</div>
    </div>

    <div id="result">
        <!-- Stock screening results will be populated here -->
    </div>

    <script>
        function startScreening() {
            const progressBar = document.getElementById('progressBar');
            const resultDiv = document.getElementById('result');

            resultDiv.innerHTML = "";  // Clear previous results

            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/screen', true);
            
            // Set up a listener for progress updates
            xhr.onprogress = function(event) {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 100;
                    progressBar.style.width = percentComplete + '%';
                    progressBar.innerHTML = Math.floor(percentComplete) + '%';
                }
            };
            
            // Handle completion of the request
            xhr.onload = function() {
                if (xhr.status === 200) {
                    progressBar.style.width = '100%';
                    progressBar.innerHTML = '100%';
                    resultDiv.innerHTML = xhr.responseText;  // Populate results
                } else {
                    progressBar.style.backgroundColor = 'red';
                    progressBar.innerHTML = 'Error!';
                }
            };

            // Handle any errors during the request
            xhr.onerror = function() {
                progressBar.style.backgroundColor = 'red';
                progressBar.innerHTML = 'Error!';
            };

            xhr.send();
        }
    </script>
</body>
</html>
