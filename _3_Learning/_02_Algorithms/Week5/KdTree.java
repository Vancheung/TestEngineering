/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.Queue;
import edu.princeton.cs.algs4.RectHV;
import edu.princeton.cs.algs4.StdDraw;

public class KdTree {

    private int size;
    private KdNode root;

    private static class KdNode {

        private Point2D point;
        private RectHV rect;
        private KdNode left;
        private KdNode right;

        public KdNode(Point2D point, RectHV rect) {

            this.point = point;
            this.rect = rect;

        }

    }

    public KdTree() {
        size = 0;
        root = null;

    }

    public boolean isEmpty()                      // is the set empty?
    {
        return size == 0;
    }

    public int size()                         // number of points in the set
    {
        return size;
    }

    public void insert(
            Point2D p)              // add the point to the set (if it is not already in the set)
    {
        // root is vertical
        root = insert(root, p, 0.0, 0.0, 1.0, 1.0, true);
    }

    public KdNode insert(KdNode node, Point2D p, double x0, double y0, double x1, double y1,
                         boolean xcmp) {
        // node: root
        if (null == node) {
            size++;
            RectHV r = new RectHV(x0, y0, x1, y1);
            return new KdNode(p, r);
        }

        // already have the same point
        else if (node.point.x() == p.x() && node.point.y() == p.y())
            return node;

        // vertical
        if (xcmp) {
            double cmp = p.x() - node.point.x();
            if (cmp < 0) // left tree
                node.left = insert(node.left, p, x0, y0, node.point.x(), y1,
                                   false); //  Change direction
            else
                node.right = insert(node.right, p, node.point.x(), y0, x1, y1, false);
        }

        // horizontal
        else {
            double cmp = p.y() - node.point.y();
            if (cmp < 0)
                node.left = insert(node.left, p, x0, y0, x1, node.point.y(), true);
            else
                node.right = insert(node.right, p, x0, node.point.y(), x1, y1, true);
        }
        return node;
    }

    public boolean contains(Point2D p)            // does the set contain point p?
    {
        return contains(root, p, true);

    }

    private boolean contains(KdNode node, Point2D p, boolean xcmp) {
        // false if you didn't find it
        if (null == node) return false;
            // true if you found it
        else if (node.point.x() == p.x() && node.point.y() == p.y()) return true;
        else {
            // The current node is vertical: compare x-coordinates
            if (xcmp) {
                double cmp = p.x() - node.point.x();
                if (cmp < 0) return contains(node.left, p, false);
                else return contains(node.right, p, false);
            }
            // The current node is horizontal: compare y-coordinates
            else {
                double cmp = p.y() - node.point.y();
                if (cmp < 0) return contains(node.left, p, true);
                else return contains(node.right, p, true);
            }
        }
    }

    public void draw()                         // draw all points to standard draw
    {
        draw(root, true);
    }

    private void draw(KdNode node, boolean xcmp) {
        if (null == node) return;
        // Draw point
        StdDraw.setPenColor(StdDraw.BLACK);
        StdDraw.setPenRadius(0.01);
        node.point.draw();
        // Draw vertical line with x-coordinates of the point and y-coordinates
        // of the parent rectangle
        if (xcmp) {
            StdDraw.setPenColor(StdDraw.RED);
            StdDraw.setPenRadius();
            StdDraw.line(node.point.x(), node.rect.ymin(), node.point.x(), node.rect.ymax());
        }
        // Draw horizontal line with y-coordinates of the point and x-coordinates
        // of the parent rectangle
        else {
            StdDraw.setPenColor(StdDraw.BLUE);
            StdDraw.setPenRadius();
            StdDraw.line(node.rect.xmin(), node.point.y(), node.rect.xmax(), node.point.y());
        }
        // Change Direction
        draw(node.left, !xcmp);
        draw(node.right, !xcmp);
    }


    public Iterable<Point2D> range(
            RectHV rect)             // all points that are inside the rectangle (or on the boundary)
    {
        Queue<Point2D> q = new Queue<Point2D>();
        range(root, rect, q);
        return q;
    }

    private void range(KdNode node, RectHV r, Queue<Point2D> q) {
        if (null == node) return;

        if (r.contains(node.point)) {
            q.enqueue(node.point);
        }

        if (r.intersects(node.rect)) {
            range(node.left, r, q);
            range(node.right, r, q);
        }
    }

    public Point2D nearest(
            Point2D p)             // a nearest neighbor in the set to point p; null if the set is empty
    {
        if (null == root) return null;
        return nearest(root, p, root.point, true);
    }

    private Point2D nearest(KdNode node, Point2D p, Point2D c, boolean xcmp) {
        Point2D closest = c;
        if (null == node)
            return closest;
        if (node.point.distanceSquaredTo(p) < closest.distanceSquaredTo(p))
            closest = node.point;
        if (node.rect.distanceSquaredTo(p) < closest.distanceSquaredTo(p)) {
            KdNode near;
            KdNode far;

            if ((xcmp && (p.x() < node.point.x())) || (!xcmp && (p.y() < node.point.y()))) {
                near = node.left;
                far = node.right;
            }
            else {
                near = node.right;
                far = node.left;
            }
            closest = nearest(near, p, closest, !xcmp);
            closest = nearest(far, p, closest, !xcmp);
        }
        return closest;
    }


    public static void main(String[] args) {

    }
}
