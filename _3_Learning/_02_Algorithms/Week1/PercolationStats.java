import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {

    public static final double ONE_POINT_96 = 1.96;
    private final double[] probability;
    private double mean = 0.0d;
    private double stddev = 0.0d;

    // perform independent trials on an n-by-n grid
    public PercolationStats(int n, int trials) {
        if (n <= 0 || trials <= 0)
            throw new IllegalArgumentException("Wrong Value! Please check your Input!");

        probability = new double[trials];


        for (int i = 0; i < trials; i++) {
            Percolation pc = new Percolation(n);
            while (!pc.percolates()) {
                pc.open(StdRandom.uniform(n), StdRandom.uniform(n));
            }
            probability[i] = (double) pc.numberOfOpenSites() / (n * n);
        }
    }

    // sample mean of percolation threshold
    public double mean() {
        if (Double.compare(0.0d, mean) == 0)
            mean = StdStats.mean(probability);
        return mean;
    }

    // sample standard deviation of percolation threshold
    public double stddev() {
        if (Double.compare(0.0d, stddev) == 0)
            stddev = StdStats.stddev(probability);
        return stddev;
    }

    // low endpoint of 95% confidence interval
    public double confidenceLo() {
        return mean - ONE_POINT_96 * stddev / Math.sqrt(probability.length);
    }

    // high endpoint of 95% confidence interval
    public double confidenceHi() {
        return mean + ONE_POINT_96 * stddev / Math.sqrt(probability.length);
    }

    // test client (see below)
    public static void main(String[] args) {
        int n = 20;
        int times = 10;
        PercolationStats stats = new PercolationStats(n, times);
        System.out.println("mean                    = " + stats.mean());
        System.out.println("stddev                  = " + stats.stddev());
        System.out.println("95% confidence interval = ["
                                   + stats.confidenceLo()
                                   + ", "
                                   + stats.confidenceHi()
                                   + "]");
    }
}

