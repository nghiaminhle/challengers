
import java.util.concurrent.atomic.AtomicInteger;

public class Queue {

	private Object[] items;
	private AtomicInteger head = new AtomicInteger(0);
	private AtomicInteger tail = new AtomicInteger(0);
	private AtomicInteger counter;
	private int size = 0;

	public Queue() {
		this(100);
	}

	public Queue(int size) {
		this.size = size;
		this.counter = new AtomicInteger(this.size);
		this.items = new Object[size];
	}

	public boolean enqueue(Object item) throws QueueFullException {
		int h = this.head.get();
		int c = this.counter.get();
		while (true) {
			if (c == 0)
				return false;
			if (this.head.compareAndSet(h, (h + 1) % this.size) && (this.counter.compareAndSet(c, c - 1))) {
				this.items[h] = item;
				return true;
			}
			c = this.counter.get();
			h = this.head.get();
		}
	}

	public Object dequeue() throws QueueFullException {
		int t = this.tail.get();
		int c = this.counter.get();
		while (true) {
			if (c == size)
				return null;
			if (this.tail.compareAndSet(t, (t + 1) % this.size) && (this.counter.compareAndSet(c, c + 1))) {
				Object item = this.items[t];
				return item;
			}
			c = this.counter.get();
			t = this.tail.get();
		}
	}
}
