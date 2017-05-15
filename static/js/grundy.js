/**
 * Created by lhurd on 5/7/17.
 */

var grundyModule = (function() {
  var my = {};
  var started = false;
  var myTurn = true;
  var numDots = 8;


  my.startUp = function() {
    document.getElementById("plus").addEventListener("click", plusClick);
    document.getElementById("minus").addEventListener("click", minusClick);
    document.getElementById("0").addEventListener("click", dotClick);

    document.getElementById("reset").addEventListener("click", resetClick);
    document.getElementById("quit").addEventListener("click", quitClick);
    if (typeof(Storage) !== 'undefined') {
        if (typeof(localStorage.numDots)  !== 'undefined') {
            numDots = localStorage.numDots;
        }
    }
    for (var i = 0; i < numDots - 1; i++) {
        plusClick();
    }
  };

  // https://zeit.co/blog/async-and-await
  function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }

  function plusClick() {
    var children = document.getElementsByClassName("dots");
    var dot = children[0].cloneNode(true);
    dot.id = children.length;
    dot.firstElementChild.addEventListener("click", dotClick);
    dot.lastElementChild.addEventListener("click", dotClick);
    document.getElementById("frame").appendChild(dot);
    document.getElementById("minus").disabled = false;
  }

  function minusClick() {
    var parent = document.getElementById("frame");
    var children = document.getElementsByClassName("dots");
    if (children.length > 1) {
      parent.removeChild(children[children.length - 1]);
    }
    if (children.length < 4) {
      document.getElementById("minus").disabled = true;
    }
  }

  function startGame() {
    if (typeof(Storage) !== 'undefined') {
        localStorage.numDots = document.getElementsByClassName("dots").length;
    }
    myTurn = true;
    started = true;
    document.getElementById("setup").style.display = "none";
    document.getElementById("quit").style.display = "inline";
  }

  function quitClick() {
    started = false;
    document.getElementById("reset").style.display = "inline";
    document.getElementById("quit").style.display = "none";
  }

  function resetClick() {
    alertText("");
    document.getElementById("setup").style.display = "inline";
    document.getElementById("reset").style.display = "none";
    var numDots = document.getElementsByClassName("dots").length;
    for (var i = 0; i < numDots - 1; i++) {
      minusClick();
    }
    setColor(0, "g1");
    for (var i = 0; i < numDots - 1; i++) {
        plusClick();
    }
    document.getElementById("minus").disabled = (numDots < 4);
  }

  function dotClick(event) {
    if (!started) {
      startGame();
    }
    if (!myTurn) {
        return;
    }
    myTurn = false;

    var numDots = document.getElementsByClassName("dots").length;
    alertText("");
    var idx = event.target.parentNode.id;
    if (!isLegal(idx)) {
      alertText("Illegal move.  Must break group into unequal pieces.");
      myTurn = true;
      return;
    } else {
      adjustColor(idx);
    }
    if (gameOver()) {
      alertText("You win!");
      quitClick();
    } else {
      sleep(1000).then(() => {
        startIdx = Math.floor(Math.random() * numDots);
      for (var i = 0; i < numDots; i++) {
        idx = (startIdx + i) % numDots;
        if (isLegal(idx)) {
          adjustColor(idx);
          break;
        }
      }
      myTurn = true;
      if (gameOver()) {
        alertText("Computer wins!");
        quitClick();
      }
      });
    }
  }

  function alertText(text) {
    document.getElementById("alertText").innerHTML = text;
  }

  function adjustColor(idx) {
    var curColor = getColor(idx);
    var newColor = incrementColor(curColor);
    var numDots = document.getElementsByClassName("dots").length;
    for (var i = idx; i < numDots; i++) {
      if (getColor(i) == curColor) {
        continue;
      } else if (getColor(i) == newColor) {
        newColor = incrementColor(newColor);
        break;
      } else {
        break;
      }
    }
    for (i = idx; i < numDots; i++) {
      if (getColor(i) == curColor) {
        setColor(i, newColor);
      } else {
        break;
      }
    }
  }

  function incrementColor(curColor) {
    if (curColor == "g1") {
      return "g2";
    } else if (curColor == "g2") {
      return "g3";
    } else {
      return "g1";
    }
  }

  function getColor(i) {
    var svgNode = document.getElementsByClassName("dots")[i];
    if (svgNode.classList.contains("g1")) {
      return "g1";
    } else if (svgNode.classList.contains("g2")) {
      return "g2";
    } else {
      return "g3";
    }
  }

  function setColor(i, c) {
    var oldColor = getColor(i);
    if (oldColor != c) {
      var svgNode = document.getElementsByClassName("dots")[i];
      svgNode.classList.add(c);
      svgNode.classList.remove(oldColor);
      if (c == "g1") {
	  svgNode.lastElementChild.innerHTML = "R";
      } else if (c == "g2") {
	  svgNode.lastElementChild.innerHTML = "G";
      } else {
	  svgNode.lastElementChild.innerHTML = "B";
      }
    }
  }

  function isLegal(idx) {
    return leftCount(idx) != 0 && leftCount(idx) != rightCount(idx);
  }

  function leftCount(idx) {
    var count = 0;
    var cur = getColor(idx);
    for (var i = idx - 1; i >= 0; i--) {
      if (getColor(i) == cur) {
        count += 1;
      } else {
        break;
      }
    }
    return count;
  }

  function rightCount(idx) {
    var count = 0;
    var cur = getColor(idx);
    var numDots = document.getElementsByClassName("dots").length;
    for (var i = idx; i < numDots; i++) {
      if (getColor(i) == cur) {
        count += 1;
      } else {
        break;
      }
    }
    return count;
  }

  function gameOver() {
    var run = 1;
    var curColor = getColor(0);
    var numDots = document.getElementsByClassName("dots").length;
    for (var i = 1; i < numDots; i++) {
      if (getColor(i) == curColor) {
        run += 1;
        if (run > 2) {
          return false;
        }
      } else {
        curColor = getColor(i);
        run = 1;
      }
    }
    return true;
  }

  return my;
})();

window.onload = grundyModule.startUp;


