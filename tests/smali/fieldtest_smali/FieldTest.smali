.class public LFieldTest;
.super Ljava/lang/Object;
.source "FieldTest.java"


# instance fields
# just testing how multiple annotations are handled in smali
# the same should apply to methods
.field private final list:Ljava/util/List;
    .annotation build Landroid/annotation/TargetApi;
        value = 0x16
    .end annotation

    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/List",
            "<",
            "Ljava/lang/String;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method public constructor <init>()V
    .registers 2

    .prologue
    .line 6
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    .line 7
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, LFieldTest;->list:Ljava/util/List;

    return-void
.end method
