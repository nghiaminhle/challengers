
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
		while (this.count < this.size) {
			if (this.flag.compareAndSet(0, 1)) {
				if (this.count++ == this.size){
					this.flag.compareAndSet(1, 0);
					return false;
				}
				this.items[this.head] = item;
				this.head = (this.head + 1) % this.size;
				this.flag.compareAndSet(1, 0);
				return true;
			}
		}
		return false;
	}

	public Object dequeue() {
		while (this.count > 0) {
			if (this.flag.compareAndSet(0, 1)) {
				if (this.count-- == 0){
					this.flag.compareAndSet(1, 0);
					return null;
				}
				Object item = this.items[this.tail];
				this.tail = (this.tail + 1) % this.size;
				this.flag.compareAndSet(1, 0);
				return item;
			}
		}
		return null;
	}
}