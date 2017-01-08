var computerWins = 0;
var humanWins = 0;
var moveNumber = 0;
var showLabels = false;

window.onload = function() {
  var winningBoards;
  var boardState;
  var boardNodes;
  var computerMovesFirst;
  document.getElementById("newGame").addEventListener('click', newGame);
  document.getElementById("plus").addEventListener('click', plusClick);
  document.getElementById("minus").addEventListener('click', minusClick);
  document.getElementById("computerFirst").addEventListener(
      'click', computerFirst);
  document.getElementById("1").addEventListener('click', bdClick);
  document.getElementById("showLabels").addEventListener('click', toggleShowLabels);
  newGame();
};

function toggleShowLabels() {
  if (showLabels) {
      document.getElementById("showLabels").innerHTML = "Show Labels";
      showLabels = false;
  } else {
      document.getElementById("showLabels").innerHTML = "Hide Labels";
      showLabels = true;
  }
}

function plusClick() {
  var parent = document.getElementById("frame");
  var children = document.getElementsByClassName("boards");
  var node = children[0].cloneNode(true);
  node.id = children.length + 1;
  node.addEventListener('click', bdClick);
  parent.appendChild(node);
  boardState.push("---------");
  boardNodes.push(node);
  initBoard(node);
  enableButton("minus", true);
}

function minusClick() {
  var parent = document.getElementById("frame");
  var children = document.getElementsByClassName("boards");
  if (children.length > 1) {
    parent.removeChild(children[children.length - 1]);
    boardState.pop();
    boardNodes.pop();
  }
  if (children.length == 1) {
    enableButton("minus", false);
  }
}

function initBoard(c) {
  var context2D = c.getContext("2d");
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
  if (checkWinning(c.id - 1)) {
    return;
  }
  if (!checkLegal(c.id - 1, i, j)) {
    return;
  }
  var context2D = c.getContext("2d");
  context2D.strokeStyle = ["red", "blue"][moveNumber % 2];
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
  context2D.strokeStyle = "black";
  if (checkWinning(c.id - 1)) {
    winningBoards++;
    boardState[c.id - 1] = "*********"
    context2D.globalAlpha = 0.5;
    context2D.fillStyle = "khaki";
    context2D.fillRect(0, 0, c.width, c.height);
    if (winningBoards == boardState.length) {
      if (isComputersTurn()) {
	    document.getElementById("status").innerHTML = "Human won...this time...";
        humanWins += 1;
        moveNumber = 0;
      } else {
	    document.getElementById("status").innerHTML = "I, for one, welcome our new computer overlords.";
	    computerWins += 1;
        moveNumber = 0;
      }
      document.getElementById("score").innerHTML = "Human: " + humanWins +
        " Computer: " + computerWins;
      return;
    }
  }
  moveNumber++;
}

function bdClick(event) {
  enableButton("computerFirst", false);
  if (isComputersTurn()) {
    return; /* It is the computer's turn. */
  }
  enableButton("newGame", true);
  enableButton("minus", false);
  enableButton("plus", false);
  drawX(event.target, Math.floor(event.layerX / 63),
    Math.floor(event.layerY / 63));
  if (isComputersTurn()) {
    getComputersMove();
  }
}

function isComputersTurn() {
  if (computerMovesFirst) {
    return moveNumber % 2 == 0;
  } else {
    return moveNumber % 2 == 1;
  }
}

function newGame() {
  if (moveNumber > 0) {
      computerWins += 1;
      document.getElementById("score").innerHTML = "Human: " + humanWins +
        " Computer: " + computerWins;
  }
  moveNumber = 0;
  computerMovesFirst = false;
  winningBoards = 0;
  enableButton("minus", false);
  enableButton("plus", true);
  enableButton("newGame", false);
  enableButton("computerFirst", true);
  var count;
  var boards = document.getElementsByClassName("boards");
  var num = boards.length;
  for (count = 0; count < num - 1; count++) {
    minusClick();
  }
  boardState = ["---------"];
  boardNodes = [boards[0]];
  for (count = 0; count < num - 1; count++) {
    plusClick();
  }
  initBoard(boards[0]);
  var status = document.getElementById("status");
  status.innerHTML = "";
}

function enableButton(name, enable) {
  var b = document.getElementById(name);
  b.disabled = !enable;
  if (enable) {
    b.className = "";
  } else {
    b.className = "disabled";
  }
}

function checkLegal(b, i, j) {
  var l = boardState[b].split("");
  if (l[i + 3 * j] == "-") {
    l[i + 3 * j] = ["x", "X"][moveNumber % 2];
    boardState[b] = l.join("");
    return true;
  } else {
    return false;
  }
}

function checkWinning(b) {
  w = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  l = boardState[b].split("");
  for (var i = 0; i < 8; i++) {
    if ((l[w[i][0]] != "-") && (l[w[i][1]] != "-") &&
      (l[w[i][2]] != "-")) {
      return true;
    }
  }
  return false;
}

function computerFirst() {
  enableButton("computerFirst", false);
  computerMovesFirst = true;
  getComputersMove()
}

function getComputersMove() {
  var stateString = boardState.join("");
  if (stateString) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
	var move = JSON.parse(this.responseText);
        drawX(boardNodes[move.board], move.column, move.row);
      }
    };
    xhttp.open("GET", "move/" + stateString, true);
    xhttp.send();
  }
}