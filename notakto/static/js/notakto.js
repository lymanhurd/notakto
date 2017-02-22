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
        getCanvas(0).addEventListener('click', bdClick);
        document.getElementById('gameStatus').addEventListener('click',
            gameStatusHandler);
        document.getElementById('gameStatus').innerHTML = 'Start';
        boardState = ['---------'];
        drawBoard(getCanvas(0));
        if (typeof(Storage) !== 'undefined') {
            for (var i = 0; i < localStorage.numBoards - 1; i++) {
                plusClick();
            }
        }
    };

    function getCanvas(i) {
        var children = document.getElementsByClassName('boards');
        return children[i].firstElementChild;
    }

    function plusClick() {
        var children = document.getElementsByClassName('boards');
        var node = children[0].cloneNode(true);
        node.firstElementChild.id = children.length;
        node.firstElementChild.addEventListener('click', bdClick);
        document.getElementById('frame').appendChild(node);
        boardState.push('---------');
        drawBoard(node.firstElementChild);
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

    function drawLine(ctx, x0, y0, x1, y1) {
        ctx.beginPath();
        ctx.moveTo(x0, y0);
        ctx.lineTo(x1, y1);
        ctx.stroke();
    }

    function drawBoard(c) {
        var context2D = c.getContext('2d');
        context2D.strokeStyle = 'black';
        context2D.globalAlpha = 1.0;
        context2D.clearRect(0, 0, c.width, c.height);
        context2D.lineWidth = 3;
        drawLine(context2D, 60, 0, 60, 185);
        drawLine(context2D, 123, 0, 123, 185);
        drawLine(context2D, 0, 60, 185, 60);
        drawLine(context2D, 0, 123, 185, 123);
    }

    function drawX(c, i, j) {
        var context2D = c.getContext('2d');
        context2D.strokeStyle = ['red', 'blue'][moveNumber % 2];
        var x = 7;
        var y = 59 - x;
        drawLine(context2D, x + 63 * i, x + 63 * j, y + 63 * i, y + 63 * j);
        drawLine(context2D, x + 63 * i, y + 63 * j, y + 63 * i, x + 63 * j);
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
            getCanvas(i).classList.remove('dead');
            drawBoard(getCanvas(i));
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
        var boardNumber = event.target.id;
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
        return true;
    }

    function checkDeadBoard(b) {
        var curBoard = boardState[b];
        for (var i = 0; i < winningBoards.length; i++) {
            if (curBoard.charAt(winningBoards[i][0]) == 'X' &&
                curBoard.charAt(winningBoards[i][1]) == 'X' &&
                curBoard.charAt(winningBoards[i][2]) == 'X') {
                boardState[b] = 'XXXXXXXXX';
                getCanvas(b).classList.add('dead');
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
        var moveIdx = monoidModule.computerMove(boardState);
        var b = Math.floor(moveIdx / 9);
        var col = moveIdx % 3;
        var row = Math.floor((moveIdx % 9) / 3);
        var board = getCanvas(b);
        drawX(board, col, row);
        checkLegal(b, col, row);
        checkDeadBoard(b, col, row);
                    moveNumber += 1;
                    checkGameOver(false);
    }
    return my;
}());
