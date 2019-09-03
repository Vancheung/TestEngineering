/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdDraw;
import edu.princeton.cs.algs4.StdOut;

import java.util.ArrayList;
import java.util.Arrays;

public class FastCollinearPoints {
    private ArrayList<LineSegment> lines;

    public FastCollinearPoints(
            Point[] points)     // finds all line segments containing 4 or more points
    {
        if (null == points)
            throw new IllegalArgumentException();
        
        Point[] jCopy = points.clone();
        Arrays.sort(jCopy);

        if (hasDuplicate(jCopy)) {
            throw new IllegalArgumentException("U have duplicate points");
        }

        lines = new ArrayList<LineSegment>();
        for (int i = 0; i < jCopy.length - 3; i++) {
            Arrays.sort(jCopy);

            // Sort the points according to the slopes they makes with p.
            // Check if any 3 (or more) adjacent points in the sorted order
            // have equal slopes with respect to p. If so, these points,
            // together with p, are collinear.

            Arrays.sort(jCopy, jCopy[i].slopeOrder());

            for (int p = 0, first = 1, last = 2; last < jCopy.length; last++) {
                // find last collinear to p point
                while (last < jCopy.length
                        && Double.compare(jCopy[p].slopeTo(jCopy[first]),
                                          jCopy[p].slopeTo(jCopy[last])) == 0) {
                    last++;
                }
                // if found at least 3 elements, make segment if it's unique
                if (last - first >= 3 && jCopy[p].compareTo(jCopy[first]) < 0) {
                    lines.add(new LineSegment(jCopy[p], jCopy[last - 1]));
                }
                // Try to find next
                first = last;
            }
        }
    }

    private boolean hasDuplicate(Point[] jCopy) {  // ordered array
        for (int i = 0; i < jCopy.length - 1; i++) {
            if (jCopy[i].compareTo(jCopy[i + 1]) == 0) {
                return true;
            }
        }
        return false;
    }


    private boolean sameas(double a, double b) {
        if (Double.compare(a, b) == 0 || Double.compare(a + b, 0.0d) == 0)
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
        // lines =  new ArrayList<LineSegment>(new HashSet<LineSegment>(lines));
        LineSegment[] segments = new LineSegment[numberOfSegments()];

        for (int i = 0; i < numberOfSegments(); i++) {
            segments[i] = lines.get(i);
        }
        return segments;

    }

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
        FastCollinearPoints collinear = new FastCollinearPoints(points);
        for (LineSegment segment : collinear.segments()) {
            StdOut.println(segment);
            segment.draw();
        }
        StdDraw.show();
    }
}
