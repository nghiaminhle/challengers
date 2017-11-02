
import java.util.concurrent.atomic.AtomicInteger;

public class RingBuffer {
	private int size;
	private volatile int head = 0;
	private volatile int tail = 0;
	private volatile int count = 0;
	private volatile int[] items;
	private AtomicInteger flag = new AtomicInteger(0);

	public RingBuffer() {
		this(100);
	}

	public RingBuffer(int size) {
		this.size = size;
		this.items = new int[this.size];
	}

	public Boolean enqueue(int item) {
		while (this.count < this.size) {
			if (this.flag.compareAndSet(0, 1)) {
				if (this.count == this.size){
					this.flag.set(0);
					return false;
				}
				this.items[this.head] = item;
				this.head = (this.head + 1) % this.size;
				this.count++;
				this.flag.set(0);
				return true;
			}
		}
		return false;
	}

	public int dequeue() {
		while (this.count > 0) {
			if (this.flag.compareAndSet(0, 1)) {
				if (this.count == 0){
					this.flag.set(0);
					return -1;
				}
				int item = this.items[this.tail];
				this.tail = (this.tail + 1) % this.size;
				this.count--;
				this.flag.set(0);
				return item;
				//return null;
			}
		}
		return -1;
	}
	
	public boolean isEmpty(){
		return this.count==0;
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