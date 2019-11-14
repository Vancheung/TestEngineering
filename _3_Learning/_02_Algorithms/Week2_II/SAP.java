import edu.princeton.cs.algs4.BreadthFirstDirectedPaths;
import edu.princeton.cs.algs4.Digraph;
import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.Stack;
import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;

public class SAP {

    private Digraph digraph;
    private final int root;


    // constructor takes a digraph (not necessarily a DAG)
    public SAP(Digraph G) {
        digraph = new Digraph(G);
        root = findRoot();
    }

    // length of shortest ancestral path between v and w; -1 if no such path
    public int length(int v, int w) {
        int anc = ancestor(v, w);
        if (anc == -1)
            return -1;
        int result = -2;

        for (int x : getAncestorPath(v, anc))
            result += 1;
        for (int x : getAncestorPath(w, anc))
            result += 1;
        return result;
    }

    // a common ancestor of v and w that participates in a shortest ancestral path; -1 if no such path
    public int ancestor(int v, int w) {
        Stack<Integer> vAncestor = getAncestor(v);
        Stack<Integer> wAncestor = getAncestor(w);
        int result = -1;
        while (!vAncestor.isEmpty() && !wAncestor.isEmpty()) {
            int x = vAncestor.pop();
            int y = wAncestor.pop();
            if (x == y)
                result = x;
            else
                break;
        }
        return result;

    }

    private Stack<Integer> getAncestor(int v) {
        validateVertex(v);
        BreadthFirstDirectedPaths BFS = new BreadthFirstDirectedPaths(digraph, v);
        Stack<Integer> result = new Stack<>();
        for (int w : BFS.pathTo(root)) {
            result.push(w);
        }
        return result;
    }

    private Iterable<Integer> getAncestorPath(int v, int w) {
        validateVertex(v);
        validateVertex(w);
        BreadthFirstDirectedPaths BFS = new BreadthFirstDirectedPaths(digraph, v);
        return BFS.pathTo(w);
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
                if (length(ans, root) < min) {
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

    int findRoot() {
        int result = -1;
        for (int v = 0; v < digraph.V(); v++) {
            if (digraph.outdegree(v) == 0)
                if (result == -1)
                    result = v;
                else
                    throw new IllegalArgumentException("Invalid hypernyms! Has more than one root");
        }
        if (result == -1)
            throw new IllegalArgumentException("Invalid hypernyms! Has no root");
        else
            return result;

    }

    // do unit testing of this class
    public static void main(String[] args) {
        In in = new In(args[0]);
        Digraph G = new Digraph(in);
        SAP sap = new SAP(G);
        while (!StdIn.isEmpty()) {
            int v = StdIn.readInt();
            // int w = StdIn.readInt();
            // int length = sap.length(v, w);
            // int ancestor = sap.ancestor(v, w);
            // StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
            StdOut.printf("path = \n");
            for (int x : sap.getAncestor(v)) {
                StdOut.printf("%d \n", x);
            }
        }
        // int v = 1;
        // int w = 9;
        // int length = sap.length(v, w);
        // int ancestor = sap.ancestor(v, w);
        // StdOut.printf("length = %d, ancestor = %d\n", length, ancestor);
    }
}
