
import java.util.concurrent.atomic.AtomicInteger;

public class RingBuffer {
	private int size;
	private int head = 0;
	private int tail = 0;
	private int count = 0;
	private Object[] items;
	private AtomicInteger flag = new AtomicInteger(0);

	public RingBuffer() {
		this(100);
	}

	public RingBuffer(int size) {
		this.size = size;
		this.items = new Object[this.size];
	}

	public Boolean enqueue(Object item) {
		int f = this.flag.get();
		while (true && this.count < this.size) {
			if (this.count == this.size)
				return false;
			if (f == 0 && this.flag.compareAndSet(f, f + 1)) {
				if (this.count == this.size)
					return false;
				this.items[this.head] = item;
				this.head = (this.head + 1) % this.size;
				this.count++;
				f = this.flag.get();
				this.flag.compareAndSet(f, f - 1);
				return true;
			}
			f = this.flag.get();
		}
		return false;
	}

	public Object dequeue() {
		int f = this.flag.get();
		while (true && this.count > 0) {
			if (this.count == 0)
				return null;
			if (f == 0 && this.flag.compareAndSet(f, f + 1)) {
				Object item = this.items[this.tail];
				this.tail = (this.tail + 1) % this.size;
				this.count--;
				f = this.flag.get();
				this.flag.compareAndSet(f, f - 1);
				return item;
			}
			f = this.flag.get();
		}
		return null;
	}
}