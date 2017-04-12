# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import codecs


class TextEdit(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.image_dict = {}
        self.num = 0
        self.setFont(QtGui.QFont("Courier", 16))

    def canInsertFromMimeData(self, source):
        return source.hasImage() or source.hasUrls() or super(TextEdit. self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        if source.hasImage():
            url = QtCore.QUrl("dropped_image_%s" % self.num)
            self.num += 1
            self.drop_image(url, source.imageData())
        elif source.hasUrls():
            for url in source.urls():
                print url.toString()
                info = QtCore.QFileInfo(url.toLocalFile())
                if QtCore.QByteArray(info.suffix()) in QtGui.QImageReader.supportedImageFormats():
                    self.drop_image(url, QtGui.QImage(info.filePath()))
                else:
                    self.drop_text_file(url)
        else:
            super(TextEdit, self).insertFromMimeData(source)

    def drop_image(self, url, image):
        if not image.isNull():
            self.document().addResource(QtGui.QTextDocument.ImageResource, url, image)
            self.textCursor().insertImage(url.toString())
            my_byte = QtCore.QByteArray()
            my_buffer = QtCore.QBuffer(my_byte)
            image.save(my_buffer, "PNG")
            self.image_dict[url.toString()] = my_byte.toBase64().data()

    def drop_text_file(self, url):
        file_path = url.toLocalFile()
        codec = QtCore.QTextCodec.codecForName("utf-8")
        with open(file_path, 'r') as f:
            self.textCursor().insertText(codec.toUnicode(f.read()))

    def to_html(self):
        tmp_str = self.toHtml()
        for key in self.image_dict.keys():
            if '<img src="%s" />' % key in tmp_str:
                tmp_str = tmp_str.replace('<img src="%s" />' % key,
                                          '<img src="data:image/png;base64,%s" />' % self.image_dict[key])
        return tmp_str.encode("utf8")

    def set_html(self, html_path):
        with codecs.open(html_path, encoding='utf-8', mode='r') as f:
            html = f.read()
            self.text_edit.setHtml(html)

    def to_image(self, image_path):
        pixmap = QtGui.QPixmap(self.document().size().toSize())
        painter = QtGui.QPainter(pixmap)
        painter.eraseRect(pixmap.rect())
        painter.begin(self)
        painter.setPen(QtCore.Qt.black)
        self.document().drawContents(painter)
        painter.end()
        pixmap.save(image_path)

    def get_images(self):
        images = list()
        b = self.text_edit.document().begin()
        while b.isValid():
            i = b.begin()
            while 1:
                if i.atEnd():
                    break
                format = i.fragment().charFormat()
                is_image = format.isImageFormat()
                if is_image:
                    images.append(format.toImageFormat().name())
                i += 1
            b = b.next()
        return images

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    tw = TextEdit()
    tw.show()
    app.exec_()
