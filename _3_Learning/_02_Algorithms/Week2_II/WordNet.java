import edu.princeton.cs.algs4.Bag;
import edu.princeton.cs.algs4.Digraph;
import edu.princeton.cs.algs4.In;

import java.util.HashMap;

public class WordNet {

    private int vertexNum;

    private final int root;
    private final SAP graphSap;

    private Digraph digraph;
    private HashMap<String, Bag<Integer>> nouns = new HashMap<>();
    private HashMap<Integer, Bag<String>> idmap = new HashMap<>();
    // constructor takes the name of the two input files

    public WordNet(String synsets, String hypernyms) {
        if (null == synsets || null == hypernyms)
            throw new IllegalArgumentException();
        readSynsets(synsets);
        digraph = new Digraph(vertexNum);
        readhyPernyms(hypernyms);
        graphSap = new SAP(digraph);
        root = graphSap.findRoot();
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
            Bag<String> words = new Bag<>();
            for (String word : linenouns) {
                if (nouns.get(word) == null)
                    nouns.put(word, new Bag<>());
                nouns.get(word).add(id);
                words.add(word);
            }
            idmap.put(id, words);
        }

    }

    public int getVertexNum() {
        return vertexNum;
    }

    public int getRoot() {
        return root;
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
        Bag<Integer> idsB  = nouns.get(nounB);

        return graphSap.length(idsA, idsB);
    }

    // a synset (second field of synsets.txt) that is the common ancestor of nounA and nounB
    // in a shortest ancestral path (defined below)
    public String sap(String nounA, String nounB) {
        if (!isNoun(nounA) || !isNoun(nounB)) throw new IllegalArgumentException();
        Bag<Integer> ancestorA = nouns.get(nounA);
        Bag<Integer> ancestorB = nouns.get(nounB);

        int ancestor = graphSap.ancestor(ancestorA, ancestorB);
        return concat(idmap.get(ancestor));

    }

    private String concat(Bag<String> strings) {
        StringBuilder sb = new StringBuilder();
        for (String s : strings) {
            sb.append(s);
        }
        return sb.toString();
    }

    // do unit testing of this class
    public static void main(String[] args) {
        String synsetsfile = "synsets15.txt";
        String hypernymsfile = "hypernyms15Tree.txt";
        WordNet wordNet = new WordNet(synsetsfile, hypernymsfile);
        assert wordNet.vertexNum == 15 : "wrong vertexNum";
        assert wordNet.root == 0 : "wrong root";
        String result = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o";
        int i = 0;
        for (String noun : wordNet.nouns()) {
            assert result.split(",")[i].equals(noun) : "wrong word";
            i += 1;
        }
        assert wordNet.isNoun("a") : "a is Noun";
        assert !wordNet.isNoun("z") : "z is not Noun";
        // assert wordNet.sap("o", "l").equals("k") : "sap is not k";
        assert wordNet.distance("h", "k") == 4 : "distance is not 4";
        assert wordNet.sap("h", "k").equals("b") : "sap is not b";
        assert wordNet.sap("o", "n").equals("n") : "sap is not n";

    }
}
