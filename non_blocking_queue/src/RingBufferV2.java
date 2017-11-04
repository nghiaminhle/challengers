
public class RingBufferV2 implements Queue {
	private int size;
	private volatile int head = 0;
	private volatile int tail = 0;
	private volatile int[] items;
	private volatile int count = 0;
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
		int b = this.head == 0 ? (size - 1) : this.head - 1;
		if (this.tail == b) {
			return false;
		}
		this.items[this.tail] = item;
		if (this.tail != b) {
			this.tail = (this.tail + 1) & (this.size - 1);
		}
		this.alert = true;
		return true;
	}

	public int dequeue() {
		if (this.tail == this.head) {
			return -1;
		}
		int item = this.items[this.head];
		if (this.head != this.tail) {
			this.head = (this.head + 1) & (this.size - 1);
		}
		this.alert = false;
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
		if (this.tail > this.head) {
			c = this.tail - this.head;
		}
		if (this.tail < this.head) {
			c = this.tail + this.size - this.head;
		}
		return c == (this.size - 1);
	}

	private boolean isPowerOf2(int maximumSize) {
		return (maximumSize & (maximumSize - 1)) == 0;
	}
}