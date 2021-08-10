.class public final LTwoWayStream;
.super Ljava/io/InputStream;
.source "src"

# instance fields
.field private a:Ljava/util/ArrayList;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/ArrayList",
            "<",
            "Ljava/lang/Integer;",
            ">;"
        }
    .end annotation
.end field

.field private b:I

.field private c:I

.field private d:I


# direct methods
.method public constructor <init>()V
    .locals 1

    .prologue
    .line 16
    invoke-direct {p0}, Ljava/io/InputStream;-><init>()V

    .line 17
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, LTwoWayStream;->a:Ljava/util/ArrayList;

    .line 18
    const/4 v0, 0x0

    iput v0, p0, LTwoWayStream;->d:I

    .line 19
    return-void
.end method


# virtual methods
.method public available()I
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 102
    iget-object v0, p0, LTwoWayStream;->a:Ljava/util/ArrayList;

    invoke-virtual {v0}, Ljava/util/ArrayList;->size()I

    move-result v0

    iget v1, p0, LTwoWayStream;->d:I

    sub-int/2addr v0, v1

    return v0
.end method

.method public close()V
    .locals 1
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 22
    const/4 v0, 0x0

    iput-object v0, p0, LTwoWayStream;->a:Ljava/util/ArrayList;

    .line 23
    return-void
.end method

.method public flush()V
    .locals 0
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 154
    return-void
.end method

.method public declared-synchronized mark(I)V
    .locals 1

    .prologue
    .line 106
    monitor-enter p0

    :try_start_1
    iput p1, p0, LTwoWayStream;->c:I

    .line 107
    iget v0, p0, LTwoWayStream;->d:I

    iput v0, p0, LTwoWayStream;->b:I
    :try_end_7
    .catchall {:try_start_1 .. :try_end_7} :catchall_9

    .line 108
    monitor-exit p0

    return-void

    .line 106
    :catchall_9
    move-exception v0

    monitor-exit p0

    throw v0
.end method

.method public markSupported()Z
    .locals 1

    .prologue
    .line 119
    const/4 v0, 0x1

    return v0
.end method

.method public read()I
    .locals 3
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 27
    iget-object v0, p0, LTwoWayStream;->a:Ljava/util/ArrayList;

    if-nez v0, :cond_c

    .line 28
    new-instance v0, Ljava/io/IOException;

    const-string v1, "Stream closed."

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 32
    :cond_c
    :try_start_c
    iget-object v0, p0, LTwoWayStream;->a:Ljava/util/ArrayList;

    iget v1, p0, LTwoWayStream;->d:I

    add-int/lit8 v2, v1, 0x1

    iput v2, p0, LTwoWayStream;->d:I

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->get(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/Integer;

    invoke-virtual {v0}, Ljava/lang/Integer;->intValue()I
    :try_end_1d
    .catch Ljava/lang/IndexOutOfBoundsException; {:try_start_c .. :try_end_1d} :catch_1f

    move-result v0

    .line 34
    :goto_1e
    return v0

    .line 33
    :catch_1f
    move-exception v0

    .line 34
    const/4 v0, -0x1

    goto :goto_1e
.end method

.method public read([B)I
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 39
    const/4 v0, 0x0

    array-length v1, p1

    invoke-virtual {p0, p1, v0, v1}, LTwoWayStream;->read([BII)I

    move-result v0

    return v0
.end method

.method public read([BII)I
    .locals 4
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    const/4 v0, -0x1

    .line 45
    if-nez p1, :cond_9

    .line 46
    new-instance v0, Ljava/lang/NullPointerException;

    invoke-direct {v0}, Ljava/lang/NullPointerException;-><init>()V

    throw v0

    .line 47
    :cond_9
    if-ltz p2, :cond_11

    if-ltz p3, :cond_11

    array-length v1, p1

    sub-int/2addr v1, p2

    if-le p3, v1, :cond_17

    .line 48
    :cond_11
    new-instance v0, Ljava/lang/IndexOutOfBoundsException;

    invoke-direct {v0}, Ljava/lang/IndexOutOfBoundsException;-><init>()V

    throw v0

    .line 49
    :cond_17
    if-nez p3, :cond_1b

    .line 50
    const/4 v0, 0x0

    .line 75
    :cond_1a
    :goto_1a
    return v0

    .line 53
    :cond_1b
    invoke-virtual {p0}, LTwoWayStream;->read()I

    move-result v2

    .line 54
    const/4 v1, 0x1

    .line 56
    if-eq v2, v0, :cond_1a

    .line 60
    int-to-byte v2, v2

    aput-byte v2, p1, p2

    .line 63
    :goto_25
    if-ge v1, p3, :cond_2d

    .line 64
    :try_start_27
    invoke-virtual {p0}, LTwoWayStream;->read()I

    move-result v2

    .line 66
    if-ne v2, v0, :cond_2f

    :cond_2d
    :goto_2d
    move v0, v1

    .line 75
    goto :goto_1a

    .line 70
    :cond_2f
    add-int v3, p2, v1

    int-to-byte v2, v2

    aput-byte v2, p1, v3
    :try_end_34
    .catch Ljava/io/IOException; {:try_start_27 .. :try_end_34} :catch_37

    .line 63
    add-int/lit8 v1, v1, 0x1

    goto :goto_25

    .line 72
    :catch_37
    move-exception v0

    goto :goto_2d
.end method

.method public declared-synchronized reset()V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 111
    monitor-enter p0

    :try_start_1
    iget v0, p0, LTwoWayStream;->b:I

    if-gez v0, :cond_10

    .line 112
    new-instance v0, Ljava/io/IOException;

    const-string v1, "Resetting to invalid mark"

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0
    :try_end_d
    .catchall {:try_start_1 .. :try_end_d} :catchall_d

    .line 111
    :catchall_d
    move-exception v0

    monitor-exit p0

    throw v0

    .line 115
    :cond_10
    :try_start_10
    iget v0, p0, LTwoWayStream;->b:I

    iput v0, p0, LTwoWayStream;->d:I
    :try_end_14
    .catchall {:try_start_10 .. :try_end_14} :catchall_d

    .line 116
    monitor-exit p0

    return-void
.end method

.method public skip(J)J
    .locals 11
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    const-wide/16 v0, 0x0

    .line 79
    cmp-long v2, p1, v0

    if-gtz v2, :cond_7

    .line 98
    :goto_6
    return-wide v0

    .line 83
    :cond_7
    const-wide/16 v2, 0x800

    invoke-static {v2, v3, p1, p2}, Ljava/lang/Math;->min(JJ)J

    move-result-wide v2

    long-to-int v4, v2

    .line 84
    new-array v5, v4, [B

    move-wide v2, p1

    .line 88
    :goto_11
    cmp-long v6, v2, v0

    if-lez v6, :cond_22

    .line 89
    const/4 v6, 0x0

    int-to-long v8, v4

    invoke-static {v8, v9, v2, v3}, Ljava/lang/Math;->min(JJ)J

    move-result-wide v8

    long-to-int v7, v8

    invoke-virtual {p0, v5, v6, v7}, LTwoWayStream;->read([BII)I

    move-result v6

    .line 91
    if-gez v6, :cond_25

    .line 98
    :cond_22
    sub-long v0, p1, v2

    goto :goto_6

    .line 95
    :cond_25
    int-to-long v6, v6

    sub-long/2addr v2, v6

    goto :goto_11
.end method

.method public write(I)V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 124
    iget-object v0, p0, LTwoWayStream;->a:Ljava/util/ArrayList;

    if-nez v0, :cond_c

    .line 125
    new-instance v0, Ljava/io/IOException;

    const-string v1, "Stream closed."

    invoke-direct {v0, v1}, Ljava/io/IOException;-><init>(Ljava/lang/String;)V

    throw v0

    .line 128
    :cond_c
    iget-object v0, p0, LTwoWayStream;->a:Ljava/util/ArrayList;

    invoke-static {p1}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 129
    return-void
.end method

.method public write([B)V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 132
    const/4 v0, 0x0

    array-length v1, p1

    invoke-virtual {p0, p1, v0, v1}, LTwoWayStream;->write([BII)V

    .line 133
    return-void
.end method

.method public write([BII)V
    .locals 2
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 138
    if-nez p1, :cond_8

    .line 139
    new-instance v0, Ljava/lang/NullPointerException;

    invoke-direct {v0}, Ljava/lang/NullPointerException;-><init>()V

    throw v0

    .line 140
    :cond_8
    if-ltz p2, :cond_18

    array-length v0, p1

    if-gt p2, v0, :cond_18

    if-ltz p3, :cond_18

    add-int v0, p2, p3

    array-length v1, p1

    if-gt v0, v1, :cond_18

    add-int v0, p2, p3

    if-gez v0, :cond_1e

    .line 142
    :cond_18
    new-instance v0, Ljava/lang/IndexOutOfBoundsException;

    invoke-direct {v0}, Ljava/lang/IndexOutOfBoundsException;-><init>()V

    throw v0

    .line 143
    :cond_1e
    if-nez p3, :cond_21

    .line 150
    :cond_20
    return-void

    .line 147
    :cond_21
    const/4 v0, 0x0

    :goto_22
    if-ge v0, p3, :cond_20

    .line 148
    add-int v1, p2, v0

    aget-byte v1, p1, v1

    invoke-virtual {p0, v1}, LTwoWayStream;->write(I)V

    .line 147
    add-int/lit8 v0, v0, 0x1

    goto :goto_22
.end method
