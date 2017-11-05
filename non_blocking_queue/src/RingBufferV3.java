import java.util.concurrent.atomic.AtomicLong;

public class RingBufferV3 implements Queue {
	private int size;
	private AtomicLong head = new PaddedAtomicLong(0);
	private AtomicLong tail = new PaddedAtomicLong(0);
	private int[] items;
	
	public RingBufferV3() {
		this(1024);
	}

	public RingBufferV3(int size) {
		if (!isPowerOf2(size)) {
			throw new RuntimeException("Maximum size must be power of 2");
		}
		this.size = size;
		this.items = new int[this.size];
	}

	public Boolean enqueue(int item) {
		long h = this.head.get();
		long t = this.tail.get();
		long b = h == 0 ? (size - 1) : h - 1;
		if (t == b) {
			return false;
		}
		this.items[(int) t] = item;
		this.tail.lazySet((t + 1) & (this.size - 1));
		return true;
	}

	public int dequeue() {
		long h = this.head.get();
		long t = this.tail.get();
		if (h == t) {
			return -1;
		}
		int item = this.items[(int) h];
		this.head.lazySet((h + 1) & (this.size - 1));
		return item;
	}

	public boolean isEmpty() {
		long h = this.head.get();
		long t = this.tail.get();
		return h == t;
	}

	public int size() {
		return this.size;
	}

	private boolean isPowerOf2(int maximumSize) {
		return (maximumSize & (maximumSize - 1)) == 0;
	}
}

class PaddedAtomicLong extends AtomicLong {
	public PaddedAtomicLong() {
	}

	public PaddedAtomicLong(final long initialValue) {
		super(initialValue);
	}

	public volatile long p1, p2, p3, p4, p5, p6 = 7;
}