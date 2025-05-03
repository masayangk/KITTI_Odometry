FROM pytorch/pytorch:2.5.1-cuda11.8-cudnn9-devel

# 環境変数設定
ENV DEBIAN_FRONTEND=noninteractive

# 必要な依存関係のインストール
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        git \
        tzdata \
        locales \
        language-pack-ja \
        ibus  \
        ibus-mozc \
        libgl1-mesa-glx \
        libglib2.0-0 \
        rsync \
        wget \
        unzip \
        sudo && \
    apt-get install -y --fix-broken && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# タイムゾーン設定
ENV TZ=Asia/Tokyo
RUN ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime && \
    dpkg-reconfigure tzdata

# ロケール設定
ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja:en \
    LC_ALL=ja_JP.UTF-8
RUN locale-gen ${LANG} && \
    update-locale LANG=${LANG}

RUN pip3 install \
        scipy==1.14.1 \
        numba \
        open3d \
        opencv-python

# ユーザー作成とsudo権限付与
ENV USER="docker"
RUN useradd -m -s /bin/bash ${USER} && \
    usermod -aG sudo ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER} && \
    echo "export PS1='\[\033[01;32m\]kitti@docker\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /home/${USER}/.bashrc

# ワークースペース設定
WORKDIR /workspace
# ユーザー切り替え
USER ${USER}
# 起動時のコマンド
CMD ["/bin/bash"] 