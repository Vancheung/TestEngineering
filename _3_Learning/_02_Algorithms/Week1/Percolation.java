import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {

    //    private WeightedQuickUnionUF uf_top;
    private final WeightedQuickUnionUF ufTopBottom;
    private final WeightedQuickUnionUF ufTop;
    private final int n, top, bottom;
    private boolean[] nodesOpen;

    // creates n-by-n grid, with all sites initially blocked
    public Percolation(int n) {
        if (n <= 0)
            throw new IllegalArgumentException("Wrong Value! Please check your Input!");

        this.n = n;
        top = 0;
        bottom = (n * n) + 1;
        //        int mapsize = this.n + 2;
        //        uf_top = new WeightedQuickUnionUF(mapsize * mapsize + 1);
        ufTopBottom = new WeightedQuickUnionUF(n * n + 2);
        ufTop = new WeightedQuickUnionUF(n * n + 1);


        nodesOpen = new boolean[this.n * this.n + 1];
        for (int i = 0; i < this.n * this.n + 1; i++)
            nodesOpen[i] = false;

    }

    // opens the site (row, col) if it is not open already
    public void open(int row, int col) {
        checkInput(row, col);

        int index = transindex(row, col);
        nodesOpen[index] = true;
        if (row == 1) {
            ufTopBottom.union(index, top);
            ufTop.union(index, top);
        }
        if (row == n)
            ufTopBottom.union(index, bottom);

        int[] around = { -1, -1, -1, -1 };
        if (validate(row - 1) && nodesOpen[transindex(row - 1, col)])
            around[0] = transindex(row - 1, col);
        if (validate(row + 1) && nodesOpen[transindex(row + 1, col)])
            around[1] = transindex(row + 1, col);
        if (validate(col - 1) && nodesOpen[transindex(row, col - 1)])
            around[2] = transindex(row, col - 1);
        if (validate(col + 1) && nodesOpen[transindex(row, col + 1)])
            around[3] = transindex(row, col + 1);
        for (int i = 0; i < around.length; i++)
            if (around[i] != -1) {
                ufTopBottom.union(index, around[i]);
                ufTop.union(index, around[i]);
            }

    }

    private void checkInput(int row, int col) {
        if (!validate(row))
            throw new IllegalArgumentException("row index must be between 1 and " + this.n + ": 0");
        if (!validate(col))
            throw new IllegalArgumentException(
                    "column index must be between 1 and " + this.n + ": 0");
    }

    // is the site (row, col) open?
    public boolean isOpen(int row, int col) {
        checkInput(row, col);
        return nodesOpen[transindex(row, col)];

    }

    // is the site (row, col) full?
    public boolean isFull(int row, int col) {
        checkInput(row, col);
        return ufTop.connected(top, transindex(row, col));
    }

    // returns the number of open sites
    public int numberOfOpenSites() {
        int count = 0;
        for (int i = 0; i < this.n * this.n + 1; i++)
            if (nodesOpen[i])
                count++;
        return count;
    }

    // does the system percolate?
    public boolean percolates() {
        return ufTopBottom.connected(top, bottom);
    }

    private boolean validate(int p) {
        //        if (false == statement)
        //            throw new IllegalArgumentException("Wrong Value! Please check your Input!");
        if (p < 1 || p > this.n)
            return false;
        return true;
    }

    private int transindex(int row, int col) {
        return (row - 1) * n + col;
    }

    // Percolation.test client (optional)
    public static void main(String[] args) {
        Percolation pc = new Percolation(3);
        // System.out.println(pc.percolates());
        pc.open(1, 3);
        System.out.println(pc.isFull(1, 3));
        pc.open(2, 3);
        System.out.println(pc.isFull(2, 3));
        pc.open(3, 3);
        System.out.println(pc.isFull(3, 3));
        System.out.println(pc.percolates());
        pc.open(3, 1);
        System.out.println(pc.isFull(3, 1));
        pc.open(2, 1);
        System.out.println(pc.isFull(3, 2));
        pc.open(1, 1);
        System.out.println(pc.isFull(3, 1));
        // System.out.println(pc.isFull(3,1));
        // System.out.println(pc.percolates());
        // System.out.println(pc.numberOfOpenSites());

    }
}
