import array

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import (QGuiApplication, QMatrix4x4, QOpenGLContext,
                         QOpenGLShader, QOpenGLShaderProgram, QSurfaceFormat, QWindow)


class OpenGLWindow(QWindow):
    def __init__(self, parent=None):
        super(OpenGLWindow, self).__init__(parent)

        self.m_update_pending = False
        self.m_animating = False
        self.m_context = None
        self.m_gl = None

        self.setSurfaceType(QWindow.OpenGLSurface)

    def initialize(self):
        pass

    def setAnimating(self, animating):
        self.m_animating = animating

        if animating:
            self.renderLater()

    def renderLater(self):
        if not self.m_update_pending:
            self.m_update_pending = True
            QGuiApplication.postEvent(self, QEvent(QEvent.UpdateRequest))

    def renderNow(self):
        if not self.isExposed():
            return

        self.m_update_pending = False

        needsInitialize = False

        if self.m_context is None:
            self.m_context = QOpenGLContext(self)
            self.m_context.setFormat(self.requestedFormat())
            self.m_context.create()

            needsInitialize = True

        self.m_context.makeCurrent(self)

        if needsInitialize:
            self.m_gl = self.m_context.versionFunctions()
            self.m_gl.initializeOpenGLFunctions()

            self.initialize()

        self.render(self.m_gl)

        self.m_context.swapBuffers(self)

        if self.m_animating:
            self.renderLater()

    def event(self, event):
        if event.type() == QEvent.UpdateRequest:
            self.renderNow()
            return True

        return super(OpenGLWindow, self).event(event)

    def exposeEvent(self, event):
        self.renderNow()

    def resizeEvent(self, event):
        self.renderNow()


class TriangleWindow(OpenGLWindow):
    vertexShaderSource = '''
attribute highp vec4 posAttr;
attribute lowp vec4 colAttr;
varying lowp vec4 col;
uniform highp mat4 matrix;
void main() {
    col = colAttr;
    gl_Position = matrix * posAttr;
}
'''

    fragmentShaderSource = '''
varying lowp vec4 col;
void main() {
    gl_FragColor = col;
}
'''

    def __init__(self):
        super(TriangleWindow, self).__init__()

        self.m_program = 0
        self.m_frame = 0

        self.m_posAttr = 0
        self.m_colAttr = 0
        self.m_matrixUniform = 0

    def initialize(self):
        self.m_program = QOpenGLShaderProgram(self)

        self.m_program.addShaderFromSourceCode(QOpenGLShader.Vertex,
                                               self.vertexShaderSource)
        self.m_program.addShaderFromSourceCode(QOpenGLShader.Fragment,
                                               self.fragmentShaderSource)

        self.m_program.link()

        self.m_posAttr = self.m_program.attributeLocation('posAttr')
        self.m_colAttr = self.m_program.attributeLocation('colAttr')
        self.m_matrixUniform = self.m_program.uniformLocation('matrix')

    def render(self, gl):
        gl.glViewport(0, 0, self.width(), self.height())

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        self.m_program.bind()

        matrix = QMatrix4x4()
        matrix.perspective(60, 4.0 / 3.0, 0.1, 100.0)
        matrix.translate(0, 0, -2)
        matrix.rotate(100.0 * self.m_frame / self.screen().refreshRate(),
                      0, 1, 0)

        self.m_program.setUniformValue(self.m_matrixUniform, matrix)

        vertices = array.array('f', [
            0.0, 0.707,
            -0.5, -0.5,
            0.5, -0.5])

        gl.glVertexAttribPointer(self.m_posAttr, 2, gl.GL_FLOAT, False, 0,
                                 vertices)
        gl.glEnableVertexAttribArray(self.m_posAttr)

        colors = array.array('f', [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0])

        gl.glVertexAttribPointer(self.m_colAttr, 3, gl.GL_FLOAT, False, 0,
                                 colors)
        gl.glEnableVertexAttribArray(self.m_colAttr)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        self.m_program.release()

        self.m_frame += 1


if __name__ == '__main__':
    import sys

    app = QGuiApplication(sys.argv)

    format = QSurfaceFormat()
    format.setSamples(4)

    window = TriangleWindow()
    window.setFormat(format)
    window.resize(640, 480)
    window.show()

    window.setAnimating(True)

    sys.exit(app.exec_())
