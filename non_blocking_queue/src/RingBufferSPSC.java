
import java.lang.reflect.Field;
import sun.misc.Unsafe;

/**
 * Ring Buffer for Single Producer and Single Consumer
 * Design for generic type
 * Use Unsafe put ordered long and access array
 */

public class RingBufferSPSC<T> {
	private int size;

	protected long p1, p2, p3, p4, p5, p6, p7;
	private volatile long head = 0;

	protected long p9, p10, p11, p12, p13, p14, p15;
	private volatile long tail = 0;

	private Object[] items;

	private static final long headOffset;
	private static final long tailOffset;
	public static final Unsafe UNSAFE;

	private static final int baseOffset;
	private static final int indexScale;

	static {
		try {
			Field f = Unsafe.class.getDeclaredField("theUnsafe");
			f.setAccessible(true);
			UNSAFE = (Unsafe) f.get(null);

			headOffset = UNSAFE.objectFieldOffset(RingBufferV2.class.getDeclaredField("head"));
			tailOffset = UNSAFE.objectFieldOffset(RingBufferV2.class.getDeclaredField("tail"));

			baseOffset = UNSAFE.arrayBaseOffset(Object[].class);
			indexScale = UNSAFE.arrayIndexScale(Object[].class);

		} catch (Exception e) {
			throw new RuntimeException(e);
		}
	}

	public RingBufferSPSC() {
		this(1024);
	}

	@SuppressWarnings("unchecked")
	public RingBufferSPSC(int size) {
		if (!isPowerOf2(size)) {
			throw new RuntimeException("Maximum size must be power of 2");
		}
		this.size = size;
		this.items = new Object[this.size];
	}

	public boolean enqueue(T item) {
		long nextTail = (tail + indexScale) & (this.size - 1);
		if (nextTail == head)
			return false;
		UNSAFE.putObject(items, baseOffset + tail, item);
		UNSAFE.putOrderedLong(this, tailOffset, nextTail);
		return true;
	}

	public T dequeue() {
		if (this.isEmpty())
			return null;
		T result = (T) UNSAFE.getObject(items, baseOffset + head);
		UNSAFE.putOrderedLong(this, headOffset, (head + indexScale) & (this.size - 1));
		return result;
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