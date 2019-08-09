import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {

    //    private WeightedQuickUnionUF uf_top;
    private WeightedQuickUnionUF uf_top_bottom;
    private int N, TOP, BOTTOM;
    private boolean[] nodes_open;

    // creates n-by-n grid, with all sites initially blocked
    public Percolation(int n) {
        if (n <= 0)
            throw new IllegalArgumentException("Wrong Value! Please check your Input!");

        N = n;
        TOP = 0;
        BOTTOM = (n * n) + 1;
//        int mapsize = this.N + 2;
//        uf_top = new WeightedQuickUnionUF(mapsize * mapsize + 1);
        uf_top_bottom = new WeightedQuickUnionUF(n * n + 2);


        nodes_open = new boolean[N * N + 1];
        for (int i = 0; i < this.N * N + 1; i++)
            nodes_open[i] = false;

    }

    // opens the site (row, col) if it is not open already
    public void open(int row, int col) {
        checkInput(row, col);

        int index = transindex(row, col);
        nodes_open[index] = true;
        if (row == 1)
            uf_top_bottom.union(TOP, index);
        if (row == N)
            uf_top_bottom.union(BOTTOM, index);

        int[] around = {-1, -1, -1, -1};
        if (validate(row - 1) && nodes_open[transindex(row - 1, col)])
            around[0] = transindex(row - 1, col);
        if (validate(row + 1) && nodes_open[transindex(row + 1, col)])
            around[1] = transindex(row + 1, col);
        if (validate(col - 1) && nodes_open[transindex(row, col - 1)])
            around[2] = transindex(row, col - 1);
        if (validate(col + 1) && nodes_open[transindex(row, col + 1)])
            around[3] = transindex(row, col + 1);
        for (int i = 0; i < 4; i++)
            if (around[i] != -1)
                uf_top_bottom.union(around[i], index);

    }

    private void checkInput(int row, int col) {
        if (false == validate(row) || (false == validate(col)))
            throw new IllegalArgumentException("Wrong Value! Please check your Input!");
    }

    // is the site (row, col) open?
    public boolean isOpen(int row, int col) {
        checkInput(row, col);
        return nodes_open[transindex(row, col)];

    }

    // is the site (row, col) full?
    public boolean isFull(int row, int col) {
        checkInput(row, col);
        return uf_top_bottom.connected(TOP, transindex(row, col));
    }

    // returns the number of open sites
    public int numberOfOpenSites() {
        int count = 0;
        for (int i = 0; i < N + 1; i++)
            if (true == nodes_open[i])
                count++;
        return count;
    }

    // does the system percolate?
    public boolean percolates() {
        return uf_top_bottom.connected(TOP, BOTTOM);
    }

    private boolean validate(int p) {
//        if (false == statement)
//            throw new IllegalArgumentException("Wrong Value! Please check your Input!");
        if (p < 1 || p > this.N)
            return false;
        return true;
    }

    private int transindex(int row, int col) {
        return (row - 1) * N + col;
    }

    // Percolation.test client (optional)
    public static void main(String[] args) {
        Percolation pc = new Percolation(4);
        System.out.println(pc.percolates());
        pc.open(2, 2);
        System.out.println(pc.percolates());
        System.out.println(pc.isFull(2,2));
        pc.open(2, 3);
        System.out.println(pc.percolates());
        System.out.println(pc.isFull(2,2));
        pc.open(1, 2);
        System.out.println(pc.percolates());
        System.out.println(pc.isFull(2,2));
        pc.open(3, 4);
        System.out.println(pc.percolates());
        System.out.println(pc.isFull(2,2));
        pc.open(4, 3);
        System.out.println(pc.percolates());
        System.out.println(pc.isFull(2,2));
        pc.open(3, 3);
        System.out.println(pc.percolates());
        System.out.println(pc.isFull(2,2));

    }
}
