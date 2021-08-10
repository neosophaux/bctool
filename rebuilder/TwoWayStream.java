import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;

// only extends InputStream to make it a valid replacement for
// the lua parser's InputStream.
public final class TwoWayStream extends InputStream {
    /* InputStream */
    private static final int MAX_SKIP_BUFFER_SIZE = 2048;

    private ArrayList<Integer> backingArray;
    private int offset;
    private int marker;
    private int marklm;

    public TwoWayStream() {
        this.backingArray = new ArrayList<>();
        this.offset = 0;
    }

    public void close() throws IOException {
        this.backingArray = null;
    }

    /* InputStream */
    public int read() throws IOException {
        if (this.backingArray == null) {
            throw new IOException("Stream closed.");
        }

        try {
            return this.backingArray.get(this.offset++);
        } catch(IndexOutOfBoundsException ex) {
            return -1;
        }
    }

    public int read(final byte[] bArray) throws IOException {
        return this.read(bArray, 0, bArray.length);
    }

    public int read(final byte[] bArray,
                    final int offset,
                    final int len) throws IOException {
        if (bArray == null) {
            throw new NullPointerException();
        } else if (offset < 0 || len < 0 || len > (bArray.length - offset)) {
            throw new IndexOutOfBoundsException();
        } else if (len == 0) {
            return 0;
        }

        int c = this.read();
        int i = 1;

        if (c == -1) {
            return -1;
        }

        bArray[offset] = (byte) c;

        try {
            for (; i < len; i++) {
                c = this.read();

                if (c == -1) {
                    break;
                }

                bArray[offset + i] = (byte) c;
            }
        } catch(IOException ex) {
        }

        return i;
    }

    public long skip(final long n) throws IOException {
        if (n <= 0) {
            return 0;
        }

        int size = (int) Math.min(TwoWayStream.MAX_SKIP_BUFFER_SIZE, n);
        byte[] skipBuffer = new byte[size];
        long remaining = n;
        int nr;

        while (remaining > 0) {
            nr = this.read(skipBuffer, 0, (int) Math.min(size, remaining));

            if (nr < 0) {
                break;
            }

            remaining -= nr;
        }

        return (n - remaining);
    }

    public int available() throws IOException {
        return (this.backingArray.size() - this.offset);
    }

    public synchronized void mark(final int readLimit) {
        this.marklm = readLimit;
        this.marker = this.offset;
    }

    public synchronized void reset() throws IOException {
        if (this.marker < 0) {
            throw new IOException("Resetting to invalid mark");
        }

        this.offset = this.marker;
    }

    public boolean markSupported() {
        return true;
    }

    /* OutputStream */
    public void write(final int b) throws IOException {
        if (this.backingArray == null) {
            throw new IOException("Stream closed.");
        }

        this.backingArray.add(b);
    }

    public void write(final byte[] bArray) throws IOException {
        this.write(bArray, 0, bArray.length);
    }

    public void write(final byte[] bArray,
                      final int offset,
                      final int len) throws IOException {
        if (bArray == null) {
            throw new NullPointerException();
        } else if ((offset < 0) || (offset > bArray.length) || (len < 0) ||
                   ((offset+ len) > bArray.length) || ((offset + len) < 0)) {
            throw new IndexOutOfBoundsException();
        } else if (len == 0) {
            return;
        }

        for (int i = 0; i < len; i++) {
            this.write(bArray[offset + i]);
        }
    }

    public void flush() throws IOException {

    }
}