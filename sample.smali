.class Lluaj/h;
.super Ljava/lang/Object;
.source "src"

# interfaces
.implements Landroid/content/DialogInterface$OnClickListener;


# instance fields
.field final synthetic a:Lluaj/g;

.field private final synthetic b:Lluaj/j;


# direct methods
.method constructor <init>(Lluaj/g;Lluaj/j;)V
    .locals 0

    .prologue
    .line 444
    iput-object p1, p0, Lluaj/h;->a:Lluaj/g;

    iput-object p2, p0, Lluaj/h;->b:Lluaj/j;

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method


# virtual methods
.method public onClick(Landroid/content/DialogInterface;I)V
    .locals 2

    .prologue
    .line 447
    iget-object v0, p0, Lluaj/h;->b:Lluaj/j;

    const/4 v1, 0x0

    iput-object v1, v0, Lluaj/j;->a:Ljava/lang/String;

    .line 448
    return-void
.end method

.annotation runtime Landroid/ext/kf$a;
    a = "a"
    b = 0x8
    c = 0x158
    d = true
.end annotation

# make sure you decompile and recompile the
# apk with apktool.
.method public static a()[I
    .locals 3
    .prologue

    const/16 v0, 0x8

    new-array v0, v0, [I

    const/16 v1, 0xf2

    const/4 v2, 0x0

    aput v1, v0, v2

    const/16 v1, 0xc2

    const/4 v2, 0x1

    aput v1, v0, v2

    const/16 v1, 0x31

    const/4 v2, 0x2

    aput v1, v0, v2

    const/16 v1, 0xf5

    const/4 v2, 0x3

    aput v1, v0, v2

    const/16 v1, 0xa8

    const/4 v2, 0x4

    aput v1, v0, v2

    const/16 v1, 0x88

    const/4 v2, 0x5

    aput v1, v0, v2

    const/16 v1, 0x15

    const/4 v2, 0x6

    aput v1, v0, v2

    const/16 v1, 0xfc

    const/4 v2, 0x7

    aput v1, v0, v2

    return-object v0
.end method