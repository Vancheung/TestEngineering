import edu.princeton.cs.algs4.StdRandom;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class RandomizedQueue<Item> implements Iterable<Item> {

    private Item[] items;
    private int n;

    // construct an empty randomized queue
    public RandomizedQueue() {
        items = (Item[]) new Object[2];
    }

    // is the randomized queue empty?
    public boolean isEmpty() {
        return n == 0;
    }

    // return the number of items on the randomized queue
    public int size() {
        return n;
    }

    private void resize(int capacity) {
        Item[] copy = (Item[]) new Object[capacity];
        for (int i = 0; i < n; i++)
            copy[i] = items[i];
        items = copy;
    }

    // add the item
    public void enqueue(Item item) {
        if (null == item) throw new IllegalArgumentException();
        if (n == items.length) resize(n * 2);
        items[n++] = item;

    }

    // remove and return a random item
    public Item dequeue() {
        if (isEmpty()) throw new IllegalArgumentException();
        int index = StdRandom.uniform(n);
        Item item = items[index];
        if (index != n - 1)
            items[index] = items[n - 1];
        items[n - 1] = null;
        n--;
        if (n < ((items.length) / 4))
            resize(items.length / 2);
        return item;

    }

    // return a random item (but do not remove it)
    public Item sample() {
        if (isEmpty()) throw new IllegalArgumentException();
        return items[StdRandom.uniform(n)];
    }

    // return an independent iterator over items in random order
    public Iterator<Item> iterator() {
        return new RandomizedQueueIterator();
    }

    private class RandomizedQueueIterator implements Iterator<Item> {
        private Item[] rdq;
        private int current;

        public RandomizedQueueIterator() {

            rdq = (Item[]) new Object[n];
            current = 0;

            for (int k = 0; k < n; k++) {
                rdq[k] = items[k];
            }

            StdRandom.shuffle(rdq);
        }

        public boolean hasNext() {
            return current < n;
        }

        public void remove() {
            throw new UnsupportedOperationException();
        }

        public Item next() {

            if (!hasNext()) throw new NoSuchElementException();
            Item it = rdq[current];
            current++;
            return it;
        }

    }

    // unit testing (required)
    public static void main(String[] args) {
        RandomizedQueue<String> rq = new RandomizedQueue();
        rq.enqueue("AAA");
        System.out.println(rq.isEmpty());
    }

}
