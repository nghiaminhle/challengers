import java.lang.reflect.Field;
import sun.misc.Unsafe;

/**
 * Ring Buffer for Single Producer and Single Consumer
 * Only for test integer
 * */

public class RingBufferV2 implements Queue {
	private int size;

	protected long p1, p2, p3, p4, p5, p6, p7;
	private volatile long head = 0;

	protected long p9, p10, p11, p12, p13, p14, p15;
	private volatile long tail = 0;

	private int[] items;

	private static final long headOffset;
	private static final long tailOffset;
	public static final Unsafe UNSAFE;
	static {
		try {
			Field f = Unsafe.class.getDeclaredField("theUnsafe");
			f.setAccessible(true);
			UNSAFE = (Unsafe) f.get(null);

			headOffset = UNSAFE.objectFieldOffset(RingBufferV2.class.getDeclaredField("head"));
			tailOffset = UNSAFE.objectFieldOffset(RingBufferV2.class.getDeclaredField("tail"));

		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	public RingBufferV2() {
		this(1024);
	}

	public RingBufferV2(int size) {
		if (!isPowerOf2(size)) {
			throw new RuntimeException("Maximum size must be power of 2");
		}
		this.size = size;
		this.items = new int[this.size];
	}

	public boolean enqueue(int item) {
		long t = this.tail;
		long nextTail = (t + 1) & (this.size - 1);
		if (nextTail == this.head) {
			return false;
		}
		this.items[(int) t] = item;
		UNSAFE.putOrderedLong(this, tailOffset, nextTail);
		return true;
	}

	public int dequeue() {
		long h = this.head;
		if (h == this.tail) {
			return -1;
		}
		int item = this.items[(int) h];
		UNSAFE.putOrderedLong(this, headOffset, (h + 1) & (this.size - 1));
		return item;
	}

	public boolean isEmpty() {
		return this.head == this.tail;
	}

	public int size() {
		return this.size;
	}

	public boolean isFull() {
		if (this.tail > this.head) {
			return (this.tail - this.head) == (this.size - 1);
		}
		if (this.tail < this.head) {
			return (this.tail + this.size - this.head) == (this.size - 1);
		}
		return false;
	}

	private boolean isPowerOf2(int maximumSize) {
		return (maximumSize & (maximumSize - 1)) == 0;
	}
}