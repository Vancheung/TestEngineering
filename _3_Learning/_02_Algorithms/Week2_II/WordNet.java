import edu.princeton.cs.algs4.Bag;
import edu.princeton.cs.algs4.Digraph;
import edu.princeton.cs.algs4.DirectedCycle;
import edu.princeton.cs.algs4.In;

import java.util.HashMap;

public class WordNet {
    private int vertexNum;
    private final SAP graphSap;

    private final Digraph digraph;
    private final HashMap<String, Bag<Integer>> nouns = new HashMap<>();
    private final HashMap<Integer, String[]> idmap = new HashMap<>();
    // constructor takes the name of the two input files

    public WordNet(String synsets, String hypernyms) {
        if (null == synsets || null == hypernyms)
            throw new IllegalArgumentException();
        readSynsets(synsets);
        digraph = new Digraph(vertexNum);
        readhyPernyms(hypernyms);
        DirectedCycle directedCycle = new DirectedCycle(digraph);
        if (directedCycle.hasCycle())
            throw new IllegalArgumentException();
        graphSap = new SAP(digraph);
    }


    private void readhyPernyms(String hypernyms) {
        In in = new In(hypernyms);
        while (in.hasNextLine()) {
            String[] token = in.readLine().split(",");
            int v = Integer.parseInt(token[0]);
            for (int i = 1; i < token.length; i++) {
                int w = Integer.parseInt(token[i]);
                digraph.addEdge(v, w);
            }
        }

    }

    private void readSynsets(String synsets) {
        In in = new In(synsets);
        while (in.hasNextLine()) {
            String[] token = in.readLine().split(",");
            int id = Integer.parseInt(token[0]);
            String[] linenouns = token[1].split(" ");
            this.vertexNum += 1;
            for (String word : linenouns) {
                if (nouns.get(word) == null)
                    nouns.put(word, new Bag<>());
                nouns.get(word).add(id);
            }
            idmap.put(id, linenouns);
        }

    }

    // returns all WordNet nouns
    public Iterable<String> nouns() {
        return nouns.keySet();
    }

    // is the word a WordNet noun?
    public boolean isNoun(String word) {
        return nouns.containsKey(word);
    }

    // distance between nounA and nounB (defined below)
    public int distance(String nounA, String nounB) {
        if (!isNoun(nounA) || !isNoun(nounB)) throw new IllegalArgumentException();
        Bag<Integer> idsA = nouns.get(nounA);
        Bag<Integer> idsB = nouns.get(nounB);

        return graphSap.length(idsA, idsB);
    }

    // a synset (second field of synsets.txt) that is the common ancestor of nounA and nounB
    // in a shortest ancestral path (defined below)
    public String sap(String nounA, String nounB) {
        if (!isNoun(nounA) || !isNoun(nounB)) throw new IllegalArgumentException();
        Bag<Integer> ancestorA = nouns.get(nounA);
        Bag<Integer> ancestorB = nouns.get(nounB);

        int ancestor = graphSap.ancestor(ancestorA, ancestorB);
        return String.join(" ", idmap.get(ancestor));

    }

    // do unit testing of this class
    public static void main(String[] args) {

    }
}
