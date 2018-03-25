package GeneralizedSudoku;

class SudokuBoard {
	private int boxes[][];
	private int values[][];
	private int fixed[][];
	private int solCount;
	private boolean counted;
	private boolean solved;
	
	public SudokuBoard(int boxes[][], int fixed[][]) {
		int i, j;
		
		this.boxes = new int[9][9];
		this.values = new int[9][9];
		this.fixed = new int[9][9];
		for (i = 0; i < 9; ++i) {
			for (j = 0; j < 9; ++j) {
				this.boxes[i][j] = boxes[i][j];
				this.fixed[i][j] = fixed[i][j];
				this.values[i][j] = fixed[i][j];
			}
		}
		this.solCount = 0;
		this.counted = false;
		this.solved = false;
	}
	
	public boolean[] getOptions(int r, int c) {
		boolean opts[] = {false, true, true, true, true, true, true, true, true, true};
		int i, j = 0;
		
		// check over the row
		i = r;
		for (j = 0; j < 9; ++j) {
			if (this.values[i][j] != 0) {
				opts[this.values[i][j]] = false;
			}
		}
		// check over the column
		j = c;
		for (i = 0; i < 9; ++i) {
			if (this.values[i][j] != 0) {
				opts[this.values[i][j]] = false;
			}
		}
		// check inside the box
		for (i = 0; i < 9; ++i) {
			for (j = 0; j < 9; ++j) {
				if (this.boxes[i][j] == this.boxes[r][c] && this.values[i][j] != 0) {
					opts[this.values[i][j]] = false;
				}
			}
		}
		
		return opts;
	}
	
	public String toString() {
		String s = "";
		int i, j;
		for (i = 0; i < 9; ++i) {
			for (j = 0; j < 9; ++j) {
				s += this.values[i][j]+" ";
			}
			s += "\n";
		}
		
		return s;
	}
	
	public void countSolutions(int r, int c) {
		if (r > 8) {
			++this.solCount;
			System.out.println(this);
			return;
		} else if (this.fixed[r][c] != 0) {
			this.countSolutions(r + (c+1)/9, (c+1)%9);
		} else {
			boolean opts[] = this.getOptions(r,  c);
			for (int i = 1; i <= 9; ++i) {
				if (opts[i]) {
					this.values[r][c] = i;
					this.countSolutions(r + (c+1)/9, (c+1)%9);
				}
			}
			this.values[r][c] = 0;
		}
	}
	
	public boolean solve() {
		if (this.solved) {
			return true;
		} else {
			return this.solve(0, 0);
		}
	}
	
	public boolean solve(int r, int c) {
		if (r > 8) {
			this.solved = true;
			return this.solved;
		} else if (this.fixed[r][c] != 0) {
			return this.solve(r + (c+1)/9, (c+1)%9);
		} else {
			boolean opts[] = this.getOptions(r,  c);
			for (int i = 1; i <= 9; ++i) {
				if (opts[i]) {
					this.values[r][c] = i;
					if (this.solve(r + (c+1)/9, (c+1)%9)) {
						return true;
					}
				}
			}
			this.values[r][c] = 0;
		}
		return false;
	}
	
	public int getSolutions() {
		if (!this.counted) {
			this.countSolutions(0, 0);
			this.counted = true;
		}
		return this.solCount;
	}
}

public class TestSudoku {

	public static void main(String[] args) {
		/*
		int fixed_values[][] = {{1, 8, 0, 0, 0, 0, 3, 0, 0},
								{0, 0, 0, 0, 7, 0, 2, 8, 0},
								{0, 0, 0, 0, 0, 4, 0, 1, 0},
								{0, 7, 0, 0, 0, 5, 0, 0, 0},
								{3, 0, 0, 7, 6, 1, 0, 0, 4},
								{0, 0, 0, 8, 0, 0, 0, 5, 0},
								{0, 3, 0, 6, 0, 0, 0, 0, 0},
								{0, 2, 6, 0, 9, 0, 0, 0, 0},
								{0, 0, 5, 0, 0, 0, 0, 3, 6}};
		
		int boxes[][] = {{1,1,1,2,2,2,3,3,3},
						{1,1,1,2,2,2,3,3,3},
						{1,1,1,2,2,2,3,3,3},
						{4,4,4,5,5,5,6,6,6},
						{4,4,4,5,5,5,6,6,6},
						{4,4,4,5,5,5,6,6,6},
						{7,7,7,8,8,8,9,9,9},
						{7,7,7,8,8,8,9,9,9},
						{7,7,7,8,8,8,9,9,9}};
		
		SudokuBoard board = new SudokuBoard(boxes, fixed_values);
		System.out.println(board);
		System.out.println(board.getSolutions());
		*/
		/*
		int good_values[][] = {{5, 3, 0, 0, 7, 0, 0, 0, 0},
								{6, 0, 0, 1, 9, 5, 0, 0, 0},
								{0, 9, 8, 0, 0, 0, 0, 6, 0},
								{8, 0, 0, 0, 6, 0, 0, 0, 3},
								{4, 0, 0, 8, 0, 3, 0, 0, 1},
								{7, 0, 0, 0, 2, 0, 0, 0, 6},
								{0, 6, 0, 0, 0, 0, 2, 8, 0},
								{0, 0, 0, 4, 1, 9, 0, 0, 5},
								{0, 0, 0, 0, 8, 0, 0, 7, 9}};

		SudokuBoard decentBoard = new SudokuBoard(boxes, good_values);
		System.out.println(decentBoard);
		System.out.println(decentBoard.getSolutions());
		System.out.println(decentBoard);
		System.out.println(decentBoard.solve());
		System.out.println(decentBoard);
		*/
		
		/*
		int weird_fixed_values[][] = {{5, 0, 0, 0, 0, 8, 7, 6, 0},
									{0, 0, 0, 4, 7, 0, 0, 3, 8},
									{0, 0, 0, 0, 0, 0, 0, 0, 0},
									{9, 0, 0, 0, 0, 0, 0, 0, 2},
									{1, 2, 3, 0, 0, 0, 9, 4, 6},
									{0, 0, 7, 0, 0, 0, 0, 0, 0},
									{0, 0, 0, 0, 0, 0, 0, 0, 0},
									{4, 8, 5, 0, 3, 2, 0, 0, 0},
									{7, 6, 2, 8, 0, 0, 0, 0, 0}};

		int weird_boxes[][] = {	{1,2,2,2,2,2,3,3,3},
								{1,2,2,2,4,4,3,3,3},
								{1,2,1,1,4,3,3,3,5},
								{1,1,1,1,4,5,5,5,5},
								{6,6,6,6,4,5,5,5,5},
								{6,6,6,6,4,8,8,8,8},
								{6,7,7,7,4,8,8,9,8},
								{7,7,7,4,4,9,9,9,8},
								{7,7,7,9,9,9,9,9,8}};
		
		SudokuBoard weirdBoard = new SudokuBoard(weird_boxes, weird_fixed_values);
		System.out.println(weirdBoard);
		System.out.println(weirdBoard.getSolutions());
		System.out.println(weirdBoard);
		System.out.println(weirdBoard.solve());
		System.out.println(weirdBoard);
		*/
		
		/*
		int weird_fixed_values2[][] = {	{0, 0, 8, 0, 0, 0, 0, 0, 2},
										{0, 0, 0, 0, 0, 0, 1, 6, 0},
										{4, 0, 0, 0, 0, 0, 0, 1, 0},
										{0, 4, 6, 0, 8, 0, 7, 0, 0},
										{1, 9, 0, 0, 0, 0, 0, 4, 3},
										{0, 0, 0, 0, 1, 0, 9, 8, 0},
										{3, 8, 0, 0, 0, 0, 0, 0, 5},
										{0, 7, 2, 0, 0, 3, 0, 0, 0},
										{6, 0, 0, 0, 3, 0, 8, 0, 4},};
		
		int weird_boxes2[][] = {{1,1,1,2,2,2,2,2,2},
								{1,1,1,4,2,3,2,3,2},
								{6,6,1,4,3,3,3,3,3},
								{6,1,1,4,5,5,5,3,3},
								{6,6,6,4,4,4,5,5,5},
								{6,7,7,4,5,5,5,8,8},
								{6,6,7,4,8,8,8,8,8},
								{7,7,7,4,9,8,9,8,9},
								{7,7,7,9,9,9,9,9,9},};
		
		SudokuBoard weirdBoard2 = new SudokuBoard(weird_boxes2, weird_fixed_values2);
		System.out.println(weirdBoard2);
		System.out.println(weirdBoard2.getSolutions());
		System.out.println(weirdBoard2.solve());
		System.out.println(weirdBoard2);
		*/
		/*
		int weird_fixed_values3[][] = {	{0, 0, 0, 5, 1, 6, 0, 0, 0},
										{1, 0, 9, 0, 0, 0, 0, 0, 0},
										{0, 0, 0, 0, 7, 0, 0, 0, 2},
										{0, 0, 1, 0, 0, 0, 0, 0, 0},
										{0, 0, 0, 0, 5, 0, 0, 0, 0},
										{0, 0, 0, 0, 0, 0, 2, 0, 0},
										{2, 0, 0, 0, 4, 0, 0, 0, 0},
										{0, 0, 0, 0, 0, 0, 6, 0, 3},
										{0, 0, 0, 7, 8, 5, 0, 0, 0}};
						
		int weird_boxes3[][] = {{1,1,1,1,2,2,2,3,3},
								{1,1,1,1,2,2,2,3,3},
								{4,4,4,1,2,6,2,2,3},
								{5,4,4,4,6,6,8,3,3},
								{5,4,4,6,6,6,8,8,3},
								{5,5,4,6,6,8,8,8,3},
								{5,7,7,6,7,9,8,8,8},
								{5,5,7,7,7,9,9,9,9},
								{5,5,7,7,7,9,9,9,9}};
						
		SudokuBoard weirdBoard3 = new SudokuBoard(weird_boxes3, weird_fixed_values3);
		System.out.println(weirdBoard3);
		System.out.println(weirdBoard3.getSolutions());
		*/
		int weird_fixed_values4[][] = {	{0, 4, 0, 0, 0, 0, 6, 0, 0},
										{0, 0, 0, 0, 0, 2, 0, 0, 0},
										{0, 9, 0, 0, 0, 0, 0, 0, 4},
										{0, 0, 9, 7, 0, 0, 0, 2, 0},
										{0, 0, 2, 0, 0, 0, 1, 0, 0},
										{0, 2, 0, 0, 0, 6, 9, 0, 0},
										{5, 0, 0, 0, 0, 0, 0, 3, 0},
										{0, 0, 0, 5, 0, 0, 0, 0, 0},
										{0, 0, 7, 0, 0, 0, 0, 5, 0},};
						
		int weird_boxes4[][] = {{1,1,1,1,1,1,1,1,2},
								{3,4,4,4,4,4,1,2,2},
								{3,3,3,3,4,4,4,2,2},
								{3,3,5,5,5,4,2,2,2},
								{3,3,5,5,5,9,9,9,2},
								{6,6,6,7,5,9,9,9,8},
								{6,6,7,7,5,5,9,9,8},
								{6,6,7,7,8,8,8,9,8},
								{6,6,7,7,7,7,8,8,8}};
						
		SudokuBoard weirdBoard4 = new SudokuBoard(weird_boxes4, weird_fixed_values4);
		System.out.println(weirdBoard4);
		System.out.println(weirdBoard4.getSolutions());
		
		System.out.println("Done");
	}

}
