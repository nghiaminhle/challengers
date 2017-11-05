import java.lang.reflect.Field;
import sun.misc.Unsafe;

public class RingBufferV2 implements Queue {
	private int size;
	private volatile int head = 0;
	private volatile int tail = 0;
	private int[] items;
	
	private static final int headOffset;
	private static final int tailOffset;
	public static final Unsafe UNSAFE;
	static {
		try {
			Field f = Unsafe.class.getDeclaredField("theUnsafe");
			f.setAccessible(true);
			UNSAFE = (Unsafe) f.get(null);

			headOffset = (int)UNSAFE.objectFieldOffset(RingBufferV2.class.getDeclaredField("head"));
			tailOffset = (int)UNSAFE.objectFieldOffset(RingBufferV2.class.getDeclaredField("tail"));
			
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

	public Boolean enqueue(int item) {
		int b = this.head == 0 ? (size - 1) : this.head - 1;
		int t = this.tail; 
		if (t == b) {
			return false;
		}
		this.items[t] = item;
		UNSAFE.putOrderedInt(this, tailOffset, (t + 1) & (this.size - 1));
		return true;
	}

	public int dequeue() {
		if (this.tail == this.head) {
			return -1;
		}
		int h = this.head;
		int item = this.items[h];
		UNSAFE.putOrderedInt(this, headOffset, (h + 1) & (this.size - 1));
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
			return (this.tail - this.head)==(this.size - 1);
		}
		if (this.tail < this.head) {
			return (this.tail + this.size - this.head)==(this.size - 1);
		}
		return false;
	}

	private boolean isPowerOf2(int maximumSize) {
		return (maximumSize & (maximumSize - 1)) == 0;
	}
}