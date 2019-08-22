import edu.princeton.cs.algs4.StdIn;
import edu.princeton.cs.algs4.StdOut;

public class Permutation {
    public static void main(String[] args) {
        RandomizedQueue<String> r = new RandomizedQueue<String>();
        int k = Integer.parseInt(args[0]);
        String s;

        while (!StdIn.isEmpty()) {
            s = StdIn.readString();
            r.enqueue(s);
        }

        int count = 0;
        for (String ss : r) {
            if (count < k) {
                StdOut.println(ss);
                count++;
            }
            else break;

        }
    }
}
