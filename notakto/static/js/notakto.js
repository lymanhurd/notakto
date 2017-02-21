var noTakToModule = (function () {
    var my = {};

    var computerWins = 0;
    var humanWins = 0;
    var moveNumber = 0;
    var boardState;

    var winningBoards = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];

    // Future expansion.
    // var labels = ['1', 'a', 'b', 'ab', 'b\xB2', 'ab\xB2', 'c', 'ac', 'bc',
    // 	      'abc', 'c\xB2', 'ac\xB2', 'bc\xB2', 'abc\xB2', 'd', 'ad',

    my.startUp = function () {
        document.getElementById('plus').addEventListener('click', plusClick);
        document.getElementById('minus').addEventListener('click', minusClick);
        document.getElementById('1').addEventListener('click', bdClick);
        document.getElementById('gameStatus').addEventListener('click',
            gameStatusHandler);
        document.getElementById('gameStatus').innerHTML = 'Start';
        boardState = ['---------'];
        drawBoard(document.getElementById('1'));
        if (typeof(Storage) !== 'undefined') {
            for (var i = 0; i < localStorage.numBoards - 1; i++) {
                plusClick();
            }
        }
    };

    function plusClick() {
        var children = document.getElementsByClassName('boards');
        var node = children[0].cloneNode(true);
        node.id = children.length + 1;
        node.addEventListener('click', bdClick);
        document.getElementById('frame').appendChild(node);
        boardState.push('---------');
        drawBoard(node);
        document.getElementById('minus').classList.remove('disabled');
    }

    function minusClick() {
        var parent = document.getElementById('frame');
        var children = document.getElementsByClassName('boards');
        if (children.length > 1) {
            parent.removeChild(children[children.length - 1]);
            boardState.pop();
        }
        if (children.length == 1) {
            document.getElementById('minus').classList.add('disabled');
        }
    }

    function drawBoard(c) {
        var context2D = c.getContext('2d');
        context2D.strokeStyle = 'black';
        context2D.globalAlpha = 1.0;
        context2D.clearRect(0, 0, c.width, c.height);
        context2D.lineWidth = 3;
        context2D.beginPath();
        context2D.moveTo(60, 0);
        context2D.lineTo(60, 185);
        context2D.stroke();
        context2D.beginPath();
        context2D.moveTo(123, 0);
        context2D.lineTo(123, 185);
        context2D.stroke();
        context2D.beginPath();
        context2D.moveTo(0, 60);
        context2D.lineTo(185, 60);
        context2D.stroke();
        context2D.beginPath();
        context2D.moveTo(0, 123);
        context2D.lineTo(185, 123);
        context2D.stroke();
    }

    function drawX(c, i, j) {
        var context2D = c.getContext('2d');
        context2D.strokeStyle = ['red', 'blue'][moveNumber % 2];
        context2D.beginPath();
        var x = 7;
        var y = 59 - x;
        context2D.moveTo(x + 63 * i, x + 63 * j);
        context2D.lineTo(y + 63 * i, y + 63 * j);
        context2D.stroke();
        context2D.beginPath();
        context2D.moveTo(x + 63 * i, y + 63 * j);
        context2D.lineTo(y + 63 * i, x + 63 * j);
        context2D.stroke();
    }

    function gameStatusHandler() {
        if (document.getElementById('gameStatus').innerHTML == 'Start') {
            startGame();
        } else {
            quitGame();
        }
    }

    function startGame() {
        if (typeof(Storage) !== 'undefined') {
            localStorage.numBoards = boardState.length;
        }
        showButton('minus', false);
        showButton('plus', false);
        document.getElementById('gameStatus').classList.remove('active');
        document.getElementById('gameStatus').innerHTML = 'Quit';
        if (isComputersTurn()) {
            getComputersMove();
        }
    }

    function quitGame() {
        if (moveNumber > 0) {
            displayScores(true);
            return;
        }
        document.getElementById('gameStatus').classList.remove('active');
        document.getElementById('gameStatus').innerHTML = 'Start';
        for (var i = 0; i < boardState.length; i++) {
            boardState[i] = '---------';
            document.getElementById((i + 1).toString()).classList.remove('dead');
            drawBoard(document.getElementById((i + 1).toString()));
        }
        showButton('minus', true);
        showButton('plus', true);
    }

    function bdClick(event) {
        if (document.getElementById('gameStatus').innerHTML == 'Start') {
            startGame();
            // If the move number has been incremented, it was the computer's turn.
            if (moveNumber == 1) {
                return;
            }
        }
        if (isComputersTurn()) {
            return;
        }
        var targetRow = Math.floor(event.layerX / 63);
        var targetCol = Math.floor(event.layerY / 63);
        var boardNumber = event.target.id - 1;
        if (!checkLegal(boardNumber, targetRow, targetCol)) {
            return;
        }
        checkDeadBoard(boardNumber, targetRow, targetCol);
        drawX(event.target, targetRow, targetCol);
        moveNumber += 1;
        if (checkGameOver(true)) {
            return;
        }
        if (!monoidModule.isWinning(boardState)) {
            document.getElementById('gameStatus').classList.add(
                'active');
        }
        getComputersMove();
    }

    function isComputersTurn() {
        return (boardState.length + moveNumber) % 2 == 0;
    }

    function displayScores(computerIsWinner) {
        if (computerIsWinner) {
            computerWins += 1;
            document.getElementById('humanScore').classList.remove('emphasized');
            document.getElementById('computerScore').classList.add('emphasized');
        } else {
            humanWins += 1;
            document.getElementById('humanScore').classList.add('emphasized');
            document.getElementById('computerScore').classList.remove('emphasized');
        }
        document.getElementById('humanScore').innerHTML = 'Human: ' + humanWins;
        document.getElementById('computerScore').innerHTML = ' Computer: ' +
            computerWins;
        moveNumber = 0;
        document.getElementById('gameStatus').innerHTML = 'Play Again';
        document.getElementById('gameStatus').classList.remove('active');
    }

    function showButton(name, enable) {
        document.getElementById(name).style.display = enable ? '' : 'none';
    }

    function checkLegal(b, i, j) {
        var idx = i + 3 * j;
        if (boardState[b].charAt(idx) != '-') {
            return false;
        }
        boardState[b] = boardState[b].slice(0, idx) + 'X' + boardState[b].substr(idx + 1);
    }

    function checkDeadBoard(b) {
        var curBoard = boardState[b];
        for (var i = 0; i < winningBoards.length; i++) {
            if (curBoard.charAt(winningBoards[i][0]) == 'X' &&
                curBoard.charAt(winningBoards[i][1]) == 'X' &&
                curBoard.charAt(winningBoards[i][2]) == 'X') {
                boardState[b] = 'XXXXXXXXX';
                document.getElementById(b + 1).classList.add('dead');
                break;
            }
        }
    }

    function checkGameOver(computerIsWinner) {
        for (var i = 0; i < boardState.length; i++) {
            if (boardState[i] != 'XXXXXXXXX') {
                return false;
            }
        }
        displayScores(computerIsWinner);
        return true;
    }

    function getComputersMove() {
        var stateString = boardState.join('');
        if (stateString) {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    var move = JSON.parse(this.responseText);
                    var board = document.getElementById(move.board + 1);
                    drawX(board, move.column, move.row);
                    checkLegal(move.board, move.column, move.row);
                    checkDeadBoard(move.board, move.column, move.row);
                    moveNumber += 1;
                    checkGameOver(false);
                }
            };
            xhttp.open('GET', 'move/' + stateString, true);
            xhttp.send();
        }
    }
    return my;
}());
