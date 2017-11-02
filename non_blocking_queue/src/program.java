
public class program {
	public static void main(String[] args) throws InterruptedException {
		RingBuffer q = new RingBuffer(1024);

		int noThreads = 1;
		int noItems = 10000000;
		test(noThreads, noItems, q);

		System.out.println("End!");
	}

	private static void test(int noThreads, int noItems, RingBuffer queue) throws InterruptedException {
		ConsumerThread[] consumers = new ConsumerThread[noThreads];
		for (int i = 0; i < consumers.length; i++) {
			consumers[i] = new ConsumerThread(queue);
			// consumers[i].setPriority(Thread.MAX_PRIORITY);
			consumers[i].start();
		}

		Thread.sleep(100);

		long start = System.nanoTime();

		int failedCount = 0;
		for (int i = 0; i < noItems; i++) {
			while (!queue.enqueue(i)) {
			}
		}

		while (!queue.isEmpty()) {
			//Thread.onSpinWait();
		}

		System.out.println("Failed count: " + failedCount);

		long elapsed = (System.nanoTime() - start) / 1000000;
		long pace = ((long) noItems) * 1000 / elapsed ;

		System.out.println("finish all " + noItems + " works at " + elapsed + "ms. Pace: " + pace + " items/s");

		start = System.nanoTime();

		for (int i = 0; i < consumers.length; i++) {
			consumers[i].cancel();
		}

		for (int i = 0; i < consumers.length; i++) {
			try {
				consumers[i].join();
			} catch (InterruptedException e) {
			}
		}

		System.out.println("all threads stopped at " + (System.nanoTime() - start) / 1000000 + "ms");
	}
}

class ConsumerThread extends Thread {

	private RingBuffer queue;

	private int counter = 0;

	public ConsumerThread(RingBuffer queue) {
		this.queue = queue;
	}

	@Override
	public void run() {
		while (!Thread.currentThread().isInterrupted()) {
			while (!Thread.currentThread().isInterrupted() && queue.isEmpty()) {
				//Thread.onSpinWait();
			}
			queue.dequeue();
			// if (item != null) counter++;
		}
	}

	public void cancel() {
		interrupt();
	}

	public int getCounter() {
		return counter;
	}
}