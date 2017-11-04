
public interface Queue {
	public Boolean enqueue(int item);
	public int dequeue();
	public boolean isEmpty();
	public boolean isFull();
	public int available();
}
