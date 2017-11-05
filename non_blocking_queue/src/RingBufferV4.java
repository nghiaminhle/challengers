
import java.util.concurrent.atomic.AtomicLong;

public class RingBufferV4 implements Queue {
	private int size;
	private AtomicLong head = new PaddedAtomicLong(0);
	private AtomicLong tail = new PaddedAtomicLong(0);
	private int[] items;
	
	public static class PaddedLong {
		public long value = 0, p1, p2, p3, p4, p5, p6;
	}

	private PaddedLong headCache = new PaddedLong();
	private PaddedLong tailCache = new PaddedLong();

	public RingBufferV4() {
		this(1024);
	}

	public RingBufferV4(int size) {
		if (!isPowerOf2(size)) {
			throw new RuntimeException("Maximum size must be power of 2");
		}
		this.size = size;
		this.items = new int[this.size];
	}

	public Boolean enqueue(int item) {
		long t = this.tail.get();
		if (t == (this.headCache.value == 0 ? (size - 1) : this.headCache.value - 1)) {
			this.headCache.value = this.head.get();
			if (t == (this.headCache.value == 0 ? (size - 1) : this.headCache.value - 1)) {
				return false;
			}
		}
		this.items[(int) t] = item;
		this.tail.lazySet((t + 1) & (this.size - 1));
		return true;
	}

	public int dequeue() {
		long h = this.head.get();
		if (h == this.tailCache.value) {
			this.tailCache.value = this.tail.get();
			if (h == this.tailCache.value) {
				return -1;
			}
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