
import java.util.concurrent.atomic.AtomicBoolean;;

public class RingBuffer {
	private int size;
	private volatile int head = 0;
	private volatile int tail = 0;
	private volatile int count = 0;
	private volatile int[] items;
	private AtomicBoolean flag = new AtomicBoolean(false);

	public RingBuffer() {
		this(100);
	}

	public RingBuffer(int size) {
		this.size = size;
		this.items = new int[this.size];
	}

	public Boolean enqueue(int item) {
		while (this.count < this.size) {
			if (this.flag.compareAndSet(false, true)) {
				try {
					if (this.count == this.size) {
						return false;
					}
					int h = this.head;
					this.items[h] = item;
					this.head = (h + 1) % this.size;
					// this.head = this.head & (this.size - 1);
					this.count++;
					return true;
				} finally {
					this.flag.set(false);
				}
			}
		}
		return false;
	}

	public int dequeue() {
		while (this.count > 0) {
			if (this.flag.compareAndSet(false, true)) {
				if (this.count == 0) {
					this.flag.set(false);
					return -1;
				}
				int t = this.tail;
				int item = this.items[t];
				this.tail = (t + 1) % this.size;
				// this.tail = this.tail & (this.size - 1);
				this.count--;
				this.flag.set(false);
				return item;
				// return -1;
			}
		}
		return -1;
	}

	public boolean isEmpty() {
		return this.count == 0;
	}

	public int size() {
		return this.size;
	}

	public int available() {
		return this.count;
	}

	public boolean isFull() {
		return this.count == this.size;
	}
}