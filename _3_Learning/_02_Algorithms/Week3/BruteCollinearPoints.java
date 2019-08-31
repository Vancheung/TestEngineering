/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Insertion;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

import java.util.ArrayList;
import java.util.Arrays;

public class BruteCollinearPoints {
    private ArrayList<LineSegment> lines;

    public BruteCollinearPoints(Point[] points)    // finds all line segments containing 4 points
    {
        if (null == points)
            throw new IllegalArgumentException();
        Arrays.sort(points);
        double[][] slopes = new double[points.length][points.length];
        lines = new ArrayList<LineSegment>();
        for (int i = 0; i < points.length; i++) {
            for (int j = i + 1; j < points.length; j++) {
                if (points[i].compareTo(points[j]) == 0)
                    throw new IllegalArgumentException("Same points!");
                slopes[i][j] = points[i].slopeTo(points[j]);
                slopes[j][i] = points[j].slopeTo(points[i]);
            }
        }
        Point startpoint, endpoint;
        // lines = new Set<LineSegment>();
        for (int p = 0; p < points.length; p++) {
            startpoint = points[p];
            endpoint = points[p];
            for (int q = p + 1; q < points.length; q++) {
                for (int r = q + 1; r < points.length; r++) {
                    for (int s = r + 1; s < points.length; s++) {
                        if (allsame(slopes[p][q], slopes[q][r], slopes[r][s], slopes[s][p])) {
                            Point[] temp = { points[p], points[q], points[r], points[s] };
                            Insertion.sort(temp);
                            LineSegment line = new LineSegment(temp[0], temp[3]);
                            // 去重
                            if (startpoint.compareTo(temp[0]) == 0
                                    && endpoint.compareTo(temp[3]) == 0)
                                continue;
                            lines.add(line);
                            startpoint = temp[0];
                            endpoint = temp[3];

                        }
                    }
                }
            }
        }
    }

    private boolean allsame(double a, double b, double c, double d) {
        if (sameas(a, b) && sameas(b, c) && sameas(c, d))
            return true;
        return false;
    }

    private boolean sameas(double a, double b) {
        if (a == b || a + b == 0)
            return true;
        return false;
    }

    public int numberOfSegments()        // the number of line segments
    {
        if (lines == null)
            throw new IllegalArgumentException();
        return lines.size();
    }

    public LineSegment[] segments() {
        if (lines == null)
            throw new IllegalArgumentException();
        LineSegment[] segments = new LineSegment[numberOfSegments()];

        for (int i = 0; i < numberOfSegments(); i++) {
            segments[i] = lines.get(i);
        }


        return segments;
    }
    // the line segments

    public static void main(String[] args) {

        // read the n points from a file
        In in = new In(args[0]);
        int n = in.readInt();
        Point[] points = new Point[n];
        for (int i = 0; i < n; i++) {
            int x = in.readInt();
            int y = in.readInt();
            points[i] = new Point(x, y);
        }

        // draw the points
        StdDraw.enableDoubleBuffering();
        StdDraw.setXscale(0, 32768);
        StdDraw.setYscale(0, 32768);
        for (Point p : points) {
            p.draw();
        }
        StdDraw.show();

        // // print and draw the line segments
        BruteCollinearPoints collinear = new BruteCollinearPoints(points);
        for (LineSegment segment : collinear.segments()) {
            StdOut.println(segment);
            segment.draw();
        }
        StdDraw.show();
    }
}
