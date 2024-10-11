pkgname=mduyt
pkgver=2024.10.10
pkgrel=1
pkgdesc="Minimalist YouTube Downloader with Qt"
arch=('x86_64')
url="https://github.com/rinechxn/mdu-yt"
license=('MIT')
depends=('pyside6' 'python' 'yt-dlp' 'ffmpeg')
makedepends=('pyinstaller')
source=("$pkgname-$pkgver.tar.gz::https://github.com/Rinechxn/mdu-yt/archive/refs/tags/$pkgver.tar.gz")
sha256sums=('SKIP')  # Replace with real checksum after download

build() {
    cd "$srcdir/$pkgname-$pkgver"
    pyinstaller --onefile --name mdu --icon=icon/raw/iconnew.png main.py  # Customize this line if needed
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    install -Dm755 "dist/mdu" "$pkgdir/usr/bin/mdu"
    install -Dm644 "icon/raw/iconnew.png" "$pkgdir/usr/share/pixmaps/mdu.png"
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

