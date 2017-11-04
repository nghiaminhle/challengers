
import java.util.concurrent.atomic.AtomicBoolean;;

public class RingBufferV2 implements Queue {
	private int size;
	private int head = 0;
	private int tail = 0;
	private int[] items;
	private volatile int count = 0;
	private AtomicBoolean flag = new AtomicBoolean(false);
	private volatile boolean alert;

	public RingBufferV2() {
		this(1024);
	}

	public RingBufferV2(int size) {
		if (!isPowerOf2(size)) {
			throw new RuntimeException("Maximum size must be power of 2");
		}
		this.alert = true;
		this.size = size;
		this.items = new int[this.size];
	}

	public Boolean enqueue(int item) {
		int b = this.tail == 0 ? (size - 1) : this.tail - 1;
		if (this.head == b) {
			return false;
		}
		this.items[this.head] = item;
		if (this.head != b) {
			this.head = (this.head + 1) & (this.size - 1);
		}
		this.alert = true;
		return true;
	}

	public int dequeue() {
		if (this.tail == this.head) {
			return -1;
		}
		int item = this.items[this.tail];
		if (this.tail != this.head) {
			this.tail = (this.tail + 1) & (this.size - 1);
		}
		return item;
	}

	public boolean isEmpty() {
		return this.head == this.tail;
	}

	public int size() {
		return this.size;
	}

	public int available() {
		return this.count;
	}

	public boolean isFull() {
		int c = 0;
		if (this.head > this.tail) {
			c = this.head - this.tail;
		}
		if (this.head < this.tail) {
			c = this.head + this.size - this.tail;
		}
		return c == (this.size - 1);
	}

	private boolean isPowerOf2(int maximumSize) {
		return (maximumSize & (maximumSize - 1)) == 0;
	}
}