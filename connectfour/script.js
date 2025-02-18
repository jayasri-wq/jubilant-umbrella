const rows = 6;
const cols = 7;
let board = Array(rows).fill().map(() => Array(cols).fill(null));
let currentPlayer = "red";
let gameOver = false;

// Create the game board
const gameBoard = document.getElementById("gameBoard");
for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
        let cell = document.createElement("div");
        cell.classList.add("cell");
        cell.dataset.row = r;
        cell.dataset.col = c;
        cell.addEventListener("click", handleMove);
        gameBoard.appendChild(cell);
    }
}

// Handle moves
function handleMove(event) {
    if (gameOver) return;
    
    let col = event.target.dataset.col;
    let row = getAvailableRow(col);
    
    if (row === -1) return;

    board[row][col] = currentPlayer;
    let cell = document.querySelector(`[data-row='${row}'][data-col='${col}']`);
    cell.classList.add(currentPlayer);

    if (checkWin(row, col)) {
        document.getElementById("status").innerText = `Player ${currentPlayer === "red" ? "1 (🔴)" : "2 (🟡)"} Wins! 🎉`;
        gameOver = true;
        return;
    }

    currentPlayer = currentPlayer === "red" ? "yellow" : "red";
    document.getElementById("status").innerText = `Player ${currentPlayer === "red" ? "1's Turn (🔴)" : "2's Turn (🟡)"}`;
}

// Get lowest available row in a column
function getAvailableRow(col) {
    for (let r = rows - 1; r >= 0; r--) {
        if (!board[r][col]) return r;
    }
    return -1;
}

// Check for a win
function checkWin(row, col) {
    return checkDirection(row, col, 1, 0) || // Vertical
           checkDirection(row, col, 0, 1) || // Horizontal
           checkDirection(row, col, 1, 1) || // Diagonal \
           checkDirection(row, col, 1, -1);  // Diagonal /
}

// Check four in a row in a given direction
function checkDirection(row, col, rowDir, colDir) {
    let color = board[row][col];
    let count = 1;
    
    for (let i = 1; i < 4; i++) {
        let r = row + rowDir * i;
        let c = col + colDir * i;
        if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] !== color) break;
        count++;
    }
    
    for (let i = 1; i < 4; i++) {
        let r = row - rowDir * i;
        let c = col - colDir * i;
        if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] !== color) break;
        count++;
    }
    
    return count >= 4;
}

// Reset game
document.getElementById("reset").addEventListener("click", () => {
    board = Array(rows).fill().map(() => Array(cols).fill(null));
    document.querySelectorAll(".cell").forEach(cell => cell.className = "cell");
    currentPlayer = "red";
    gameOver = false;
    document.getElementById("status").innerText = "Player 1's Turn (🔴)";
});
