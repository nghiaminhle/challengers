
public class program {

	public static void main(String[] args) throws Exception {
		// Queue q = new RingBuffer(1024 * 1024 * 16); // 1024*1024
		// Queue q = new RingBufferV2(1024 * 1024); // 1024*1024

		Queue q = new RingBufferV2(1024 * 1024);
		for (int r = 0; r < 100; r++) {
			System.out.println(r);

			int noThreads = 1;
			int noItems = 10000000;
			test(noThreads, noItems, q);
		}

		/*
		 * for(int i=0; i<20;i++){ q.enqueue(i);
		 * System.out.println(q.dequeue()); }
		 */
		System.out.println("-End!-");
	}

	private static void test(int noThreads, int noItems, Queue queue) throws InterruptedException {
		ConsumerThread[] consumers = new ConsumerThread[noThreads];
		for (int i = 0; i < consumers.length; i++) {
			consumers[i] = new ConsumerThread(queue);
			consumers[i].start();
		}

		Thread.sleep(100);

		long start = System.nanoTime();

		for (int i = 0; i < noItems; i++) {
			while (!queue.enqueue(i)) {
				// System.out.println(i + "-is full:" + queue.isFull());
			}
			// queue.enqueue(i);
		}

		while (!queue.isEmpty()) {
			// Thread.onSpinWait();
			// System.out.println("is empty:" + queue.isEmpty());
		}

		long elapsed = (System.nanoTime() - start) / 1000000;
		long pace = ((long) noItems) * 1000 / elapsed;

		System.out.println("finish all " + noItems + " works at " + elapsed + "ms. Pace: " + pace + " items/s");

		start = System.nanoTime();

		for (int i = 0; i < consumers.length; i++) {
			consumers[i].cancel();
		}

		for (int i = 0; i < consumers.length; i++) {
			try {
				consumers[i].join();
				long counter = consumers[i].getCounter();
				System.out.println(counter);
				if (counter != 49999995000000L) {
					System.out.println("failed");
				}
			} catch (InterruptedException e) {
			}
		}

		System.out.println("all threads stopped at " + (System.nanoTime() - start) / 1000000 + "ms");
	}
}

class ConsumerThread extends Thread {

	private Queue queue;

	public ConsumerThread(Queue queue) {
		this.queue = queue;
	}

	private long counter = 0;

	@Override
	public void run() {
		while (!Thread.currentThread().isInterrupted()) {
			while (!Thread.currentThread().isInterrupted() && queue.isEmpty()) {
				// Thread.onSpinWait();
			}
			int item = queue.dequeue();
			if (item != -1) {
				counter += item;
			}
			// if (item != null) counter++;
		}
	}

	public void cancel() {
		interrupt();
	}

	public long getCounter() {
		return counter;
	}
}