import edu.princeton.cs.algs4.BreadthFirstDirectedPaths;
import edu.princeton.cs.algs4.Digraph;
import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;

public class SAP {

    private final Digraph digraph;


    // constructor takes a digraph (not necessarily a DAG)
    public SAP(Digraph G) {
        digraph = new Digraph(G);

    }

    // length of shortest ancestral path between v and w; -1 if no such path
    public int length(int v, int w) {
        validateVertex(v);
        validateVertex(w);
        int anc = ancestor(v, w);
        if (anc == -1) {
            return -1;
        }
        BreadthFirstDirectedPaths vBFS = new BreadthFirstDirectedPaths(digraph, v);
        BreadthFirstDirectedPaths wBFS = new BreadthFirstDirectedPaths(digraph, w);
        return vBFS.distTo(anc) + wBFS.distTo(anc);
    }

    // a common ancestor of v and w that participates in a shortest ancestral path; -1 if no such path
    public int ancestor(int v, int w) {
        validateVertex(v);
        validateVertex(w);
        BreadthFirstDirectedPaths vBFS = new BreadthFirstDirectedPaths(digraph, v);
        BreadthFirstDirectedPaths wBFS = new BreadthFirstDirectedPaths(digraph, w);
        // if (vBFS.hasPathTo(w) && wBFS.hasPathTo(v))  // has cycle
        //     return vBFS.distTo(w) < wBFS.distTo(v) ? v : w;
        // if (vBFS.hasPathTo(w))
        //     return w;
        // if (wBFS.hasPathTo(v))
        //     return v;
        int anc = -1;
        int minLength = Integer.MAX_VALUE;
        for (int u = 0; u < digraph.V(); ++u) {
            if (vBFS.hasPathTo(u) && wBFS.hasPathTo(u)) {
                int dist = vBFS.distTo(u) + wBFS.distTo(u);
                if (dist < minLength) {
                    minLength = dist;
                    anc = u;
                }
            }
        }
        return anc;


    }

    // length of shortest ancestral path between any vertex in v and any vertex in w; -1 if no such path
    public int length(Iterable<Integer> v, Iterable<Integer> w) {
        int min = digraph.V() + 1;
        for (int x : v) {
            for (int y : w) {
                int len = length(x, y);
                if (len == -1)
                    throw new IllegalArgumentException();
                min = len < min ? len : min;
            }
        }
        if (min == digraph.V() + 1)
            return -1;
        return min;
    }

    // a common ancestor that participates in shortest ancestral path; -1 if no such path
    public int ancestor(Iterable<Integer> v, Iterable<Integer> w) {
        int result = -1;
        int min = digraph.V() + 1;
        for (int x : v) {
            for (int y : w) {
                int ans = ancestor(x, y);
                if (ans == -1) throw new IllegalArgumentException();
                if (length(x, y) < min) {
                    result = ans;
                    min = length(x, ans) < length(y, ans) ? length(x, ans) : length(y, ans);
                }
            }
        }
        return result;
    }

    private void validateVertex(int v) {
        if (v < 0 || v >= digraph.V())
            throw new IllegalArgumentException(
                    "vertex " + v + " is not between 0 and " + (digraph.V() - 1));
    }


    // do unit testing of this class
    public static void main(String[] args) {
        In in = new In(args[0]);
        Digraph G = new Digraph(in);
        SAP sap = new SAP(G);
        while (!StdIn.isEmpty()) {
            int v = StdIn.readInt();
            int w = StdIn.readInt();
            int length = sap.length(v, w);
            int ancestor = sap.ancestor(v, w);
            StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
            StdOut.printf("path = \n");
        }
        // int v = 1;
        // int w = 9;
        // int length = sap.length(v, w);
        // int ancestor = sap.ancestor(v, w);
        // StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
    }
}
