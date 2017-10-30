
import java.util.concurrent.atomic.AtomicInteger;

public class RingBuffer {
	private int size;
	private AtomicInteger head = new AtomicInteger(-1);
	private AtomicInteger tail = new AtomicInteger(-1);
	private Object[] items;
	private AtomicInteger[] atomicItems;

	public RingBuffer() {
		this(100);
	}

	public RingBuffer(int size) {
		this.size = size;
		this.items = new Object[this.size];
		this.atomicItems = new AtomicInteger[this.size];
		for (int i = 0; i < this.size; i++) {
			this.atomicItems[i] = new AtomicInteger(0);
		}
	}

	public boolean enqueue(Object item) {
		int h = this.head.get();
		int v = this.atomicItems[(h + 1) % this.size].get();
		if (v == 0 && this.atomicItems[(h + 1) % this.size].compareAndSet(v, v + 1)) {
			this.items[(h + 1) % this.size] = item;
			while (!this.head.compareAndSet(h, (h + 1) % this.size)) {
				h = this.head.get();
			}
			return true;
		}
		return false;
	}

	public Object dequeue() {
		int t = this.tail.get();
		int v = this.atomicItems[(t + 1) % this.size].get();
		if (v == 1 && this.atomicItems[(t + 1) % this.size].compareAndSet(v, v - 1)) {
			Object item = this.items[(t + 1) % this.size];
			while (!this.tail.compareAndSet(t, (t + 1) % this.size)) {
				t = this.tail.get();
			}
			return item;
		}
		return null;
	}
}
