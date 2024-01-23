# !/usr/bin/python

import sys
# importing Qt widgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import QFileInfo

# import fitz
from fitz import fitz, Rect

# importing numpy and pandas
import numpy as np
import pandas as pd

# importing PyQtGraph
import pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import *

import os
from functools import partial


class Window(QMainWindow):
    """Main Window."""

    def __init__(self):
        """Initializer."""
        super().__init__()
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()

        """Variables"""
        self.path = None  # path of opened signal file
        self.time1 = [i for i in range(0, 500)]
        self.time2 = [i for i in range(0, 500)]

        self.data_channel_1 = [0]
        self.data_channel_2 = [0]
        self.data_channel_3 = [0]
        self.data_channel_4 = [0]
        self.data_channel_5 = [0]
        self.data_channel_6 = [0]
        self.existChannel = [0, 0, 0, 0, 0, 0]
        self.plot1Status = True
        self.plot2Status = True

        self.data_channel_live_1 = list()
        self.data_channel_live_2 = list()
        self.data_channel_live_3 = list()
        self.data_channel_live_4 = list()
        self.data_channel_live_5 = list()
        self.data_channel_live_6 = list()
        self.time_live1 = list()
        self.time_live2 = list()

        self.speed = 50
        self.speed1 = 50
        self.speed2 = 50

        self.snapshots = list()
        self.snapshotNumber = 0

        """main properties"""
        # setting icon to the window
        self.setWindowIcon(QIcon('images/icon.png'))

        # setting title
        self.setWindowTitle("ICU Signal Viewer")

        # UI contents
        self._createMenuBar()
        self.initUI()

        # Status Bar
        # self.statusBar = QStatusBar()
        # self.statusBar.setStyleSheet("font-size:13px; padding: 3px; color: black; font-weight:900")
        # self.statusBar.showMessage("Welcome to our application...")
        # self.setStatusBar(self.statusBar)

    def initUI(self):
        """Window GUI contents"""
        wid = QWidget(self)
        self.setGeometry(120, 80, 1200, 800)
        self.setStyleSheet("background-color:#B6D0E2")
        self.setCentralWidget(wid)
        # setting configuration options
        pg.setConfigOptions(antialias=True)

        # big Layout
        outerLayout = QVBoxLayout()

        ControlsLayout = QHBoxLayout()

        ControlsLayoutUnlinked = QHBoxLayout()

        Graph1Controls = QVBoxLayout()
        Graph2Controls = QVBoxLayout()

        ControlsLayoutUnlinked.addLayout(Graph1Controls)
        ControlsLayoutUnlinked.addLayout(Graph2Controls)
        # Create a layout for the plots
        plotsLayout = QVBoxLayout()

        graphsLayout = QHBoxLayout()

        self.positive_x_range = [0, 60000]
        y_range = [-2, 2]

        def checkLimits1():
            vb = self.PlotGraph1.getViewBox()
            if vb.viewRange()[1][0] < y_range[0]:
                vb.setRange(yRange=(y_range[0], y_range[1]))
            elif vb.viewRange()[1][1] > y_range[1]:
                vb.setRange(yRange=(y_range[0], y_range[1]))

            if vb.viewRange()[0][0] < self.positive_x_range[0]:
                vb.setRange(
                    xRange=(self.positive_x_range[0], self.positive_x_range[1]))
            elif vb.viewRange()[0][1] > self.positive_x_range[1]:
                vb.setRange(
                    xRange=(self.positive_x_range[0], self.positive_x_range[1]))

        def checkLimits2():
            vb = self.PlotGraph2.getViewBox()
            if vb.viewRange()[1][0] < y_range[0]:
                vb.setRange(yRange=(y_range[0], y_range[1]))
            elif vb.viewRange()[1][1] > y_range[1]:
                vb.setRange(yRange=(y_range[0], y_range[1]))

            if vb.viewRange()[0][0] < self.positive_x_range[0]:
                vb.setRange(
                    xRange=(self.positive_x_range[0], self.positive_x_range[1]))
            elif vb.viewRange()[0][1] > self.positive_x_range[1]:
                vb.setRange(
                    xRange=(self.positive_x_range[0], self.positive_x_range[1]))

        # creating graphics layout widget
        self.GrLayout1 = pg.GraphicsLayoutWidget()
        self.GrLayout1.setMinimumSize(400, 300)
        self.PlotGraph1 = self.GrLayout1.addPlot()
        self.PlotGraph1.showGrid(x=True, y=True)
        self.PlotGraph1.setTitle("Port 1", color="white", size="18pt")
        self.PlotGraph1.setLabel('bottom', 'Time', '')

        # Can't drag plot 1 after the limits
        # self.PlotGraph1.setYRange(y_range[0], y_range[1])
        # self.PlotGraph1.setXRange(self.positive_x_range[0], self.positive_x_range[1])
        # self.PlotGraph1.setLimits(yMin=y_range[0], yMax=y_range[1])
        # self.PlotGraph1.getViewBox().setMouseEnabled(y=False)
        # self.PlotGraph1.setLimits(
        #     xMin=self.positive_x_range[0], xMax=self.positive_x_range[1])
        # self.PlotGraph1.getViewBox().setMouseEnabled(x=False)
        self.PlotGraph1.sigRangeChanged.connect(checkLimits1)

        self.GrLayout1.setBackground('#0f0f0f')
        self.PlotGraph1.getAxis('left').setPen("#FFFFFF")
        self.PlotGraph1.getAxis('bottom').setPen("#FFFFFF")

        # Add legend
        self.legendItemName1 = self.PlotGraph1.addLegend()
        self.legendItemName1.anchor(1, 1)

        self.GrLayout2 = pg.GraphicsLayoutWidget()
        self.GrLayout2.setMinimumSize(400, 300)
        self.PlotGraph2 = self.GrLayout2.addPlot()
        self.PlotGraph2.showGrid(x=True, y=True)
        self.PlotGraph2.setTitle("Port 2", color="white", size="18pt")
        self.PlotGraph2.setLabel('bottom', 'Time', '')

        self.PlotGraph2.sigRangeChanged.connect(checkLimits2)

        self.GrLayout2.setBackground('#0f0f0f')
        self.PlotGraph2.getAxis('left').setPen("#FFFFFF")
        self.PlotGraph2.getAxis('bottom').setPen("#FFFFFF")

        self.PlotGraph2.setXRange(
            self.positive_x_range[0], self.positive_x_range[1])

        self.PlotGraph2.setXLink(self.PlotGraph1)
        self.PlotGraph2.setYLink(self.PlotGraph1)

        graphsLayout.addWidget(self.GrLayout1)
        graphsLayout.addWidget(self.GrLayout2)
        outerLayout.addLayout(graphsLayout)
        outerLayout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Expanding))

        def linkGraphs():
            if self.linkCheckbox.isChecked():
                self.linkWidget.setCurrentIndex(0)
                self.timer1.setInterval(int(1*(100-self.speed)))
                self.timer2.setInterval(int(1*(100-self.speed)))
            else:
                self.linkWidget.setCurrentIndex(1)
                self.timer1.setInterval(int(1*(100-self.speed1)))
                self.timer2.setInterval(int(1*(100-self.speed2)))

        # CheckBox for linking
        self.linkCheckbox = QCheckBox("Linked")
        self.linkCheckbox.setChecked(True)
        font = QFont('Sans', 14)
        checkbox_style = """
              QCheckBox {
                padding: 5px;
            }

            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator:unchecked {
                background-color:red;
            }

            QCheckBox::indicator:checked {
                background-color:#16F529;
            }
        """
        self.linkCheckbox.setFont(font)
        self.linkCheckbox.setStyleSheet(checkbox_style)
        self.checkBoxLayout = QHBoxLayout()
        self.checkBoxLayout.addStretch(1)
        self.checkBoxLayout.addWidget(self.linkCheckbox)
        self.checkBoxLayout.addStretch(1)
        self.linkCheckbox.stateChanged.connect(linkGraphs)

        outerLayout.addLayout(self.checkBoxLayout)

        outerLayout.addSpacerItem(QSpacerItem(0, -20, QSizePolicy.Expanding))
        # Add legend
        self.legendItemName2 = self.PlotGraph2.addLegend()
        self.legendItemName2.anchor(1, 1)

        # Plot and return the line of the signal to manipulate it.
        self.data_line_ch1 = self.PlotGraph1.plot(
            self.time_live1, self.data_channel_live_1, name="Channel 1", pen="g")
        self.data_line_ch2 = self.PlotGraph1.plot(
            self.time_live1, self.data_channel_live_2, name="Channel 2", pen="purple")
        self.data_line_ch3 = self.PlotGraph1.plot(
            self.time_live1, self.data_channel_live_3, name="Channel 3", pen=(173, 216, 230))
        self.data_line_ch4 = self.PlotGraph2.plot(
            self.time_live2, self.data_channel_live_4, name="Channel 4", pen="g")
        self.data_line_ch5 = self.PlotGraph2.plot(
            self.time_live2, self.data_channel_live_5, name="Channel 5", pen="purple")
        self.data_line_ch6 = self.PlotGraph2.plot(
            self.time_live2, self.data_channel_live_6, name="Channel 6", pen=(173, 216, 230))
        # Set shadow to the channels
        self.data_line_ch1.setShadowPen("green")
        self.data_line_ch2.setShadowPen("purple")
        self.data_line_ch3.setShadowPen("blue")
        self.data_line_ch4.setShadowPen("green")
        self.data_line_ch5.setShadowPen("purple")
        self.data_line_ch6.setShadowPen("blue")
        # Update The plot
        self._updatePlot1()
        self._updatePlot2()

        # Create a layout for the main buttons
        mainButtonsLayout = QHBoxLayout()

        mainButtonsLayout.addSpacerItem(
            QSpacerItem(450, 10, QSizePolicy.Expanding))

        def pausePlay():
            if not (self.plot1Status and self.plot2Status):
                self.timer1.start()
                self.timer2.start()
                self.plot1Status = True
                self.plot2Status = True
                self.PlayBtn.setIcon(QIcon("images/pause.ico"))
                # self.statusBar.showMessage("Plot is running.. You can't add any signal while plot is running.")
            else:
                self.timer1.stop()
                self.timer2.stop()
                self.plot1Status = False
                self.plot2Status = False
                self.PlayBtn.setIcon(QIcon("images/play.ico"))
                # self.statusBar.showMessage("Plot is paused.")

        def pausePlay1():
            if not self.plot1Status:
                self.timer1.start()
                self.plot1Status = True
                self.PlayBtn1.setIcon(QIcon("images/pause.ico"))
                # self.statusBar.showMessage("Plot is running.. You can't add any signal while plot is running.")
            else:
                self.timer1.stop()
                self.plot1Status = False
                self.PlayBtn1.setIcon(QIcon("images/play.ico"))
                # self.statusBar.showMessage("Plot is paused.")

        def pausePlay2():
            if not self.plot2Status:
                self.timer2.start()
                self.plot2Status = True
                self.PlayBtn2.setIcon(QIcon("images/pause.ico"))
                # self.statusBar.showMessage("Plot is running.. You can't add any signal while plot is running.")
            else:
                self.timer2.stop()
                self.plot2Status = False
                self.PlayBtn2.setIcon(QIcon("images/play.ico"))
                # self.statusBar.showMessage("Plot is paused.")

        def link_plots(linked):
            if linked:
                self.PlotGraph2.setXLink(self.PlotGraph1)
                self.PlotGraph2.setYLink(self.PlotGraph1)
            else:
                self.PlotGraph2.setXLink(None)
                self.PlotGraph2.setYLink(None)

        self.linkCheckbox.stateChanged.connect(link_plots)

        # PauseAndPlay
        self.PlayBtn = QPushButton()
        self.PlayBtn.setIcon(QIcon("images/play.ico"))
        self.PlayBtn.clicked.connect(pausePlay)
        # Reset Button
        self.resetButton = QPushButton()
        self.resetButton.setIcon(QIcon("images/reset.svg"))
        self.resetButton.clicked.connect(self.rewindSignal)

        # Unlinked Buttons
        self.PlayBtn1 = QPushButton()
        self.PlayBtn1.setIcon(QIcon("images/play.ico"))
        self.PlayBtn1.clicked.connect(pausePlay1)
        self.PlayBtn1.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")

        self.resetButton1 = QPushButton()
        self.resetButton1.setIcon(QIcon("images/reset.svg"))
        self.resetButton1.setStyleSheet(
            "font-size:14px; background-color:#800020; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.resetButton1.clicked.connect(self.rewindSignal1)

        self.gridShowBtn1 = QCheckBox("Show Grid", self)
        self.gridShowBtn1.setChecked(True)
        self.gridShowBtn1.setStyleSheet("font-size:14px;")
        self.gridShowBtn1.stateChanged.connect(self.showGrid1)
        grid1ShowLayout = QHBoxLayout()
        grid1ShowLayout.addStretch(1)
        grid1ShowLayout.addWidget(self.gridShowBtn1)
        grid1ShowLayout.addStretch(1)

        buttonslayout1 = QHBoxLayout()
        buttonslayout1.addStretch(1)
        buttonslayout1.addWidget(self.PlayBtn1)
        buttonslayout1.addWidget(self.resetButton1)
        buttonslayout1.addStretch(1)

        self.PlayBtn2 = QPushButton()
        self.PlayBtn2.setIcon(QIcon("images/play.ico"))
        self.PlayBtn2.clicked.connect(pausePlay2)
        self.PlayBtn2.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")

        self.resetButton2 = QPushButton()
        self.resetButton2.setIcon(QIcon("images/reset.svg"))
        self.resetButton2.setStyleSheet(
            "font-size:14px; background-color:#800020; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.resetButton2.clicked.connect(self.rewindSignal2)

        self.gridShowBtn2 = QCheckBox("Show Grid", self)
        self.gridShowBtn2.setChecked(True)
        self.gridShowBtn2.setStyleSheet("font-size:14px;")
        self.gridShowBtn2.stateChanged.connect(self.showGrid2)
        grid2ShowLayout = QHBoxLayout()
        grid2ShowLayout.addStretch(1)
        grid2ShowLayout.addWidget(self.gridShowBtn2)
        grid2ShowLayout.addStretch(1)

        buttonslayout2 = QHBoxLayout()
        buttonslayout2.addStretch(1)
        buttonslayout2.addWidget(self.PlayBtn2)
        buttonslayout2.addWidget(self.resetButton2)
        buttonslayout2.addStretch(1)

        # Grid Button
        self.gridShowBtn = QCheckBox("Show Grid", self)
        self.gridShowBtn.setChecked(True)
        self.gridShowBtn.setStyleSheet("font-size:14px;")
        self.gridShowBtn.stateChanged.connect(self.showGrid)

        # StyleSheet
        # downSpeedBtn.setStyleSheet("font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px; background: black")
        self.PlayBtn.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.resetButton.setStyleSheet(
            "font-size:14px; background-color:#800020; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")

        # mainButtonsLayout.addWidget(downSpeedBtn,2)
        mainButtonsLayout.addWidget(self.PlayBtn, 2)
        mainButtonsLayout.addWidget(self.resetButton, 2)

        mainButtonsLayout.addSpacerItem(
            QSpacerItem(450, 10, QSizePolicy.Expanding))

        # Tab widget for linking
        self.linkedLayout = QHBoxLayout()
        self.linkWidget = QTabWidget()
        self.tab1 = QWidget()
        self.tab1Layout = QVBoxLayout()
        self.tab2 = QWidget()
        self.tab2Layout = QVBoxLayout()
        self.tab1.setLayout(self.tab1Layout)
        self.tab2.setLayout(self.tab2Layout)
        self.linkWidget.addTab(self.tab1, "Linked")
        self.linkWidget.addTab(self.tab2, "Unlinked")
        self.linkedLayout.addWidget(self.linkWidget)

        # Hide the tab bar of the tab widget
        tabBar = self.linkWidget.tabBar()
        tabBar.setFixedHeight(0)

        outerLayout.addLayout(self.linkedLayout)

        def SpeedSliderChange(value):
            self.speed = value
            self.timer1.setInterval(int(1*(100-self.speed)))
            self.timer2.setInterval(int(1*(100-self.speed)))
            self.speedValueLabel.setText(str(value))

        def SpeedSliderChange1(value):
            self.speed1 = value
            self.speedValueLabel1.setText(str(value))
            self.timer1.setInterval(int(1*(100-self.speed1)))

        def SpeedSliderChange2(value):
            self.speed2 = value
            self.speedValueLabel2.setText(str(value))
            self.timer2.setInterval(int(1*(100-self.speed2)))

        # Linked speed Slider
        speedSliderLayout = QHBoxLayout()
        sliderLabel = QLabel("Speed: ")
        sliderLabel.setStyleSheet(
            "font-size: 13px;padding: 2px;font-weight: 800;")

        self.SpeedSlider = QSlider(Qt.Horizontal, self)
        self.SpeedSlider.setValue(self.speed1)
        self.SpeedSlider.valueChanged[int].connect(SpeedSliderChange)

        self.speedValueLabel = QLabel("50")
        self.speedValueLabel.setStyleSheet(
            "font-size: 13px;padding: 2px;font-weight: 800;")

        speedSliderLayout.addSpacerItem(
            (QSpacerItem(30, 10, QSizePolicy.Expanding)))
        speedSliderLayout.addWidget(sliderLabel, 1)
        speedSliderLayout.addWidget(self.SpeedSlider, 10)
        speedSliderLayout.addWidget(self.speedValueLabel, 1)
        speedSliderLayout.addSpacerItem(
            (QSpacerItem(30, 10, QSizePolicy.Expanding)))

        # Unlinked Speed Sliders
        # Slider 1
        speedSlider1Layout = QHBoxLayout()
        slider1Label = QLabel("Speed: ")
        slider1Label.setStyleSheet(
            "font-size: 13px;padding: 2px;font-weight: 800;")

        self.SpeedSlider1 = QSlider(Qt.Horizontal, self)
        self.SpeedSlider1.setValue(self.speed1)
        self.SpeedSlider1.valueChanged[int].connect(SpeedSliderChange1)

        self.speedValueLabel1 = QLabel("50")
        self.speedValueLabel1.setStyleSheet(
            "font-size: 13px;padding: 2px;font-weight: 800;")

        speedSlider1Layout.addSpacerItem(
            (QSpacerItem(10, 10, QSizePolicy.Expanding)))
        speedSlider1Layout.addWidget(slider1Label, 1)
        speedSlider1Layout.addWidget(self.SpeedSlider1, 10)
        speedSlider1Layout.addWidget(self.speedValueLabel1, 1)
        speedSlider1Layout.addSpacerItem(
            (QSpacerItem(10, 10, QSizePolicy.Expanding)))

        # Slider 2
        speedSlider2Layout = QHBoxLayout()
        slider2Label = QLabel("Speed: ")
        slider2Label.setStyleSheet(
            "font-size: 13px;padding: 2px;font-weight: 800;")

        self.SpeedSlider2 = QSlider(Qt.Horizontal, self)
        self.SpeedSlider2.setValue(self.speed2)
        self.SpeedSlider2.valueChanged[int].connect(SpeedSliderChange2)

        self.speedValueLabel2 = QLabel("50")
        self.speedValueLabel2.setStyleSheet(
            "font-size: 13px;padding: 2px;font-weight: 800;")

        speedSlider2Layout.addSpacerItem(
            (QSpacerItem(30, 10, QSizePolicy.Expanding)))
        speedSlider2Layout.addWidget(slider2Label, 1)
        speedSlider2Layout.addWidget(self.SpeedSlider2, 10)
        speedSlider2Layout.addWidget(self.speedValueLabel2, 1)
        speedSlider2Layout.addSpacerItem(
            (QSpacerItem(10, 10, QSizePolicy.Expanding)))

        Graph1Controls.addLayout(speedSlider1Layout)
        Graph1Controls.addLayout(buttonslayout1)
        Graph1Controls.addLayout(grid1ShowLayout)

        Graph2Controls.addLayout(speedSlider2Layout)
        Graph2Controls.addLayout(buttonslayout2)
        Graph2Controls.addLayout(grid2ShowLayout)

        # plotsLayout.addLayout(speedSliderLayout)
        self.tab1Layout.addLayout(speedSliderLayout, 1)
        self.tab1Layout.addLayout(ControlsLayout, 1)
        self.tab2Layout.addLayout(ControlsLayoutUnlinked, 1)
        plotsLayout.addLayout(mainButtonsLayout)
        plotsLayout.addWidget(self.gridShowBtn)

        # Top layout of the graph
        ControlsLayout.addLayout(plotsLayout, 2)

        # Create a layout for the buttons for specific signal
        ChannelbuttonsLayout = QHBoxLayout()
        # Add some buttons to the layout
        self.tabs = QTabWidget()
        self.tabs.activateWindow()
        self.tabs.setStyleSheet("font-size:15px;")

        ChannelbuttonsLayout.addWidget(self.tabs)

        allDockArea = DockArea()

        # give this dock the minimum possible size
        plotArea = Dock("Plot", size=(1, 1))

        plotArea.addWidget(self.GrLayout1)
        plotArea.addWidget(self.GrLayout2)
        plotArea.hideTitleBar()

        outerLayout.addLayout(ControlsLayout, 1)
        outerLayout.addLayout(ChannelbuttonsLayout, 1)

        wid.setLayout(outerLayout)

    # Create a menu bar
    def _createMenuBar(self):
        """MenuBar"""
        toolbar = QToolBar("ICU Toolbar")
        self.addToolBar(toolbar)

        menuBar = self.menuBar()

        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)

        openF = QAction("Open 1", self)
        openF.setShortcut("Ctrl+1")
        fileMenu.addAction(openF)
        openF.triggered.connect(self.browse_Signal1)

        openF2 = QAction("Open 2", self)
        openF2.setShortcut("Ctrl+2")
        fileMenu.addAction(openF2)
        openF2.triggered.connect(self.browse_Signal2)

        Snapshot = QAction("Snapshot", self)
        Snapshot.setShortcut("Ctrl+s")
        fileMenu.addAction(Snapshot)
        Snapshot.triggered.connect(self.takeSnapshot)

        exportS = QAction("Export", self)
        exportS.setShortcut("Ctrl+e")
        fileMenu.addAction(exportS)
        exportS.triggered.connect(self.exportPDF)

        quit = QAction("Quit", self)
        quit.setShortcut("Ctrl+q")
        fileMenu.addAction(quit)
        quit.triggered.connect(self.exit)

        menuBar.addMenu(fileMenu)

    def update_view_range(self, plot, time_live):
        xRange = 150
        if len(time_live) < xRange:
            plot.setXRange(0, xRange, padding=0)
        if len(time_live) > xRange:
            plot.setXRange(max(time_live), max(time_live)-xRange, padding=0)

    # Main Plot
    def _updatePlot1(self):
        self.incrementTimeAlongSignalRun1 = 1
        if self.existChannel[0] == 1 or self.existChannel[1] == 1 or self.existChannel[2] == 1:
            self.timer1.setInterval((int(1*(100-self.speed1))))
            self.timer1.timeout.connect(self.update_plot1_data)
            self.timer1.start()
            self.PlayBtn1.setIcon(QIcon("images/pause.ico"))

    def _updatePlot2(self):
        self.incrementTimeAlongSignalRun2 = 1
        if self.existChannel[3] == 1 or self.existChannel[4] == 1 or self.existChannel[5] == 1:
            self.timer2.setInterval((int(1*(100-self.speed2))))
            self.timer2.timeout.connect(self.update_plot2_data)
            self.timer2.start()
            self.PlayBtn2.setIcon(QIcon("images/pause.ico"))

    def update_plot1_data(self):
        if len(self.time_live1) < len(self.time1) - 1:
            self.time_live1.append(self.time1[len(self.time_live1)])
            if self.existChannel[0] != 0:
                self.data_channel_live_1.append(
                    self.data_channel_1[len(self.time_live1)])
                # Update the data.
                self.data_line_ch1.setData(
                    self.time_live1, self.data_channel_live_1)

            if self.existChannel[1] != 0:
                self.data_channel_live_2.append(
                    self.data_channel_2[len(self.time_live1)])
                # Update the data.
                self.data_line_ch2.setData(
                    self.time_live1, self.data_channel_live_2)

            if self.existChannel[2] != 0:
                self.data_channel_live_3.append(
                    self.data_channel_3[len(self.time_live1)])
                # Update the data.
                self.data_line_ch3.setData(
                    self.time_live1, self.data_channel_live_3)

            self.incrementTimeAlongSignalRun1 += 1
            self.update_view_range(self.PlotGraph1, self.time_live1)
            self.setLimits()

    def update_plot2_data(self):
        if len(self.time_live2) < len(self.time2) - 1:
            self.time_live2.append(self.time2[len(self.time_live2)])
            if self.existChannel[3] != 0:
                self.data_channel_live_4.append(
                    self.data_channel_4[len(self.time_live2)])
                # Update the data.
                self.data_line_ch4.setData(
                    self.time_live2, self.data_channel_live_4)

            if self.existChannel[4] != 0:
                self.data_channel_live_5.append(
                    self.data_channel_5[len(self.time_live2)])
                # Update the data.
                self.data_line_ch5.setData(
                    self.time_live2, self.data_channel_live_5)

            if self.existChannel[5] != 0:
                self.data_channel_live_6.append(
                    self.data_channel_6[len(self.time_live2)])
                # Update the data.
                self.data_line_ch6.setData(
                    self.time_live2, self.data_channel_live_6)
            self.incrementTimeAlongSignalRun2 += 1
            if self.linkCheckbox.isChecked():
                self.update_view_range(self.PlotGraph2, self.time_live1)
            else:
                self.update_view_range(self.PlotGraph2, self.time_live2)
            self.setLimits()

    # Show grid

    def showGrid(self):
        if self.gridShowBtn.isChecked():
            self.PlotGraph1.showGrid(x=True, y=True)
            self.PlotGraph2.showGrid(x=True, y=True)
        else:
            self.PlotGraph1.showGrid(x=False, y=False)
            self.PlotGraph2.showGrid(x=False, y=False)

    def showGrid1(self):
        if self.gridShowBtn1.isChecked():
            self.PlotGraph1.showGrid(x=True, y=True)
        else:
            self.PlotGraph1.showGrid(x=False, y=False)

    def showGrid2(self):
        if self.gridShowBtn2.isChecked():
            self.PlotGraph2.showGrid(x=True, y=True)
        else:
            self.PlotGraph2.showGrid(x=False, y=False)

    # Plot channel of the signal.

    def plotChannelSignal(self, Channel, x, y, plotname, color="w"):
        pen = pg.mkPen(color=color)
        data_line_channel = Channel.plot(x, y, name=plotname, pen=pen)
        return data_line_channel

    # Add Tabs
    def channelTabUI1(self):
        """Create the General page UI."""
        chTabUI1Tab = QWidget()
        if self.existChannel[0] == 0:
            chTabUI1Tab.setDisabled(True)

        buttonsLayout = QHBoxLayout()

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        # Color Button Changer
        colorbtn = pg.ColorButton()
        self.changeColorBtn(self.data_line_ch1, colorbtn)
        ColorLabel = QLabel("Color:")
        ColorLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(ColorLabel, 1)
        buttonsLayout.addWidget(colorbtn, 1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        # Title Box Changer
        TitleLabel = QLabel("Label:")
        TitleLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(TitleLabel, 1)

        TitleBox = QLineEdit(self)
        TitleBox.setStyleSheet(
            "font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        TitleBox.setText("Channel 1")
        buttonsLayout.addWidget(TitleBox, 4)

        changeTitleBtn = QPushButton("Change Label")
        changeTitleBtn.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        changeTitleBtn.clicked.connect(
            partial(self.changeTitle, self.data_line_ch1, TitleBox, self.PlotGraph1))
        buttonsLayout.addWidget(changeTitleBtn, 2)

        movePlots = QPushButton("Move Plots")
        movePlots.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        movePlots.clicked.connect(lambda: self.moveSignal(0))
        buttonsLayout.addWidget(movePlots)
        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        # Hide/show the signal
        self.HideCheckBoxChannel1 = QCheckBox("Hide", self)
        self.HideCheckBoxChannel1.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(self.HideCheckBoxChannel1, 1)
        self.HideCheckBoxChannel1.stateChanged.connect(self.hideShowSignal1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.clearChannel1 = QPushButton()
        self.clearChannel1.setIcon(QIcon("images/clear.svg"))
        self.clearChannel1.setStyleSheet(
            "background: black; font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.clearChannel1.clicked.connect(partial(self.signalClear, 0))
        buttonsLayout.addWidget(self.clearChannel1, 1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        chTabUI1Tab.setLayout(buttonsLayout)
        return chTabUI1Tab

    def channelTabUI2(self):
        """Create the Network page UI."""
        chTabUI2Tab = QWidget()
        if self.existChannel[1] == 0:
            chTabUI2Tab.setDisabled(False)

        buttonsLayout = QHBoxLayout()

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        colorbtn = pg.ColorButton()
        self.changeColorBtn(self.data_line_ch2, colorbtn)
        ColorLabel = QLabel("Color:")
        ColorLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(ColorLabel, 1)
        buttonsLayout.addWidget(colorbtn, 1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        TitleLabel = QLabel("Label:")
        TitleLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(TitleLabel, 1)

        TitleBox = QLineEdit(self)
        TitleBox.setStyleSheet(
            "font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        TitleBox.setText("Channel 2")
        buttonsLayout.addWidget(TitleBox, 4)

        changeTitleBtn = QPushButton("Change Label")
        changeTitleBtn.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        changeTitleBtn.clicked.connect(
            partial(self.changeTitle, self.data_line_ch2, TitleBox, self.PlotGraph1))
        buttonsLayout.addWidget(changeTitleBtn, 2)

        movePlots = QPushButton("Move Plots")
        movePlots.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        movePlots.clicked.connect(lambda: self.moveSignal(1))
        buttonsLayout.addWidget(movePlots)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.HideCheckBoxChannel2 = QCheckBox("Hide", self)
        self.HideCheckBoxChannel2.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(self.HideCheckBoxChannel2, 1)

        # connecting it to function
        self.HideCheckBoxChannel2.stateChanged.connect(self.hideShowSignal2)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.clearChannel2 = QPushButton()
        self.clearChannel2.setIcon(QIcon("images/clear.svg"))
        self.clearChannel2.setStyleSheet(
            "background: black; font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.clearChannel2.clicked.connect(partial(self.signalClear, 1))
        buttonsLayout.addWidget(self.clearChannel2, 1)
        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))
        chTabUI2Tab.setLayout(buttonsLayout)
        return chTabUI2Tab

    def channelTabUI3(self):
        """Create the Network page UI."""
        chTabUI3Tab = QWidget()
        if self.existChannel[2] == 0:
            chTabUI3Tab.setDisabled(True)
        buttonsLayout = QHBoxLayout()

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        colorbtn = pg.ColorButton()
        self.changeColorBtn(self.data_line_ch3, colorbtn)
        ColorLabel = QLabel("Color:")
        ColorLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(ColorLabel, 1)
        buttonsLayout.addWidget(colorbtn, 1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        TitleLabel = QLabel("Label:")
        TitleLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(TitleLabel, 1)

        TitleBox = QLineEdit(self)
        TitleBox.setStyleSheet(
            "font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        TitleBox.setText("Channel 3")
        buttonsLayout.addWidget(TitleBox, 4)

        changeTitleBtn = QPushButton("Change Label")
        changeTitleBtn.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        changeTitleBtn.clicked.connect(
            partial(self.changeTitle, self.data_line_ch3, TitleBox, self.PlotGraph1))
        buttonsLayout.addWidget(changeTitleBtn, 2)

        movePlots = QPushButton("Move Plots")
        movePlots.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        movePlots.clicked.connect(lambda: self.moveSignal(2))
        buttonsLayout.addWidget(movePlots)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.HideCheckBoxChannel3 = QCheckBox("Hide", self)
        self.HideCheckBoxChannel3.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(self.HideCheckBoxChannel3, 1)

        # connecting it to function
        self.HideCheckBoxChannel3.stateChanged.connect(self.hideShowSignal3)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.clearChannel3 = QPushButton()
        self.clearChannel3.setIcon(QIcon("images/clear.svg"))
        self.clearChannel3.setStyleSheet(
            "background: black; font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.clearChannel3.clicked.connect(partial(self.signalClear, 2))
        buttonsLayout.addWidget(self.clearChannel3, 1)
        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))
        chTabUI3Tab.setLayout(buttonsLayout)
        return chTabUI3Tab

    def channelTabUI4(self):
        """Create the Network page UI."""
        chTabUI4Tab = QWidget()
        if self.existChannel[3] == 0:
            chTabUI4Tab.setDisabled(True)

        buttonsLayout = QHBoxLayout()

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        colorbtn = pg.ColorButton()
        self.changeColorBtn(self.data_line_ch4, colorbtn)
        ColorLabel = QLabel("Color:")
        ColorLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(ColorLabel, 1)
        buttonsLayout.addWidget(colorbtn, 1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        TitleLabel = QLabel("Label:")
        TitleLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(TitleLabel, 1)

        TitleBox = QLineEdit(self)
        TitleBox.setStyleSheet(
            "font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        TitleBox.setText("Channel 4")
        buttonsLayout.addWidget(TitleBox, 4)

        changeTitleBtn = QPushButton("Change Label")
        changeTitleBtn.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        changeTitleBtn.clicked.connect(
            partial(self.changeTitle, self.data_line_ch4, TitleBox, self.PlotGraph2))
        buttonsLayout.addWidget(changeTitleBtn, 2)

        movePlots = QPushButton("Move Plots")
        movePlots.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        movePlots.clicked.connect(lambda: self.moveSignal(3))
        buttonsLayout.addWidget(movePlots)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.HideCheckBoxChannel4 = QCheckBox("Hide", self)
        self.HideCheckBoxChannel4.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(self.HideCheckBoxChannel4, 1)

        # connecting it to function
        self.HideCheckBoxChannel4.stateChanged.connect(self.hideShowSignal4)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.clearChannel4 = QPushButton()
        self.clearChannel4.setIcon(QIcon("images/clear.svg"))
        self.clearChannel4.setStyleSheet(
            "background: black; font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.clearChannel4.clicked.connect(partial(self.signalClear, 3))
        buttonsLayout.addWidget(self.clearChannel4, 1)
        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))
        chTabUI4Tab.setLayout(buttonsLayout)
        return chTabUI4Tab

    def channelTabUI5(self):
        """Create the Network page UI."""
        chTabUI5Tab = QWidget()
        if self.existChannel[4] == 0:
            chTabUI5Tab.setDisabled(True)

        buttonsLayout = QHBoxLayout()

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        colorbtn = pg.ColorButton()
        self.changeColorBtn(self.data_line_ch5, colorbtn)
        ColorLabel = QLabel("Color:")
        ColorLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(ColorLabel, 1)
        buttonsLayout.addWidget(colorbtn, 1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        TitleLabel = QLabel("Label:")
        TitleLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(TitleLabel, 1)

        TitleBox = QLineEdit(self)
        TitleBox.setStyleSheet(
            "font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        TitleBox.setText("Channel 5")
        buttonsLayout.addWidget(TitleBox, 4)

        changeTitleBtn = QPushButton("Change Label")
        changeTitleBtn.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        changeTitleBtn.clicked.connect(
            partial(self.changeTitle, self.data_line_ch5, TitleBox, self.PlotGraph2))
        buttonsLayout.addWidget(changeTitleBtn, 2)

        movePlots = QPushButton("Move Plots")
        movePlots.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        movePlots.clicked.connect(lambda: self.moveSignal(4))
        buttonsLayout.addWidget(movePlots)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.HideCheckBoxChannel5 = QCheckBox("Hide", self)
        self.HideCheckBoxChannel5.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(self.HideCheckBoxChannel5, 1)

        # connecting it to function
        self.HideCheckBoxChannel5.stateChanged.connect(self.hideShowSignal5)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.clearChannel5 = QPushButton()
        self.clearChannel5.setIcon(QIcon("images/clear.svg"))
        self.clearChannel5.setStyleSheet(
            "background: black; font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.clearChannel5.clicked.connect(partial(self.signalClear, 4))
        buttonsLayout.addWidget(self.clearChannel5, 1)
        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))
        chTabUI5Tab.setLayout(buttonsLayout)
        return chTabUI5Tab

    def channelTabUI6(self):
        """Create the Network page UI."""
        chTabUI6Tab = QWidget()
        if self.existChannel[5] == 0:
            chTabUI6Tab.setDisabled(True)

        buttonsLayout = QHBoxLayout()

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        colorbtn = pg.ColorButton()
        self.changeColorBtn(self.data_line_ch6, colorbtn)
        ColorLabel = QLabel("Color:")
        ColorLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(ColorLabel, 1)
        buttonsLayout.addWidget(colorbtn, 1)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        TitleLabel = QLabel("Label:")
        TitleLabel.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(TitleLabel, 1)

        TitleBox = QLineEdit(self)
        TitleBox.setStyleSheet(
            "font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        TitleBox.setText("Channel 6")
        buttonsLayout.addWidget(TitleBox, 4)

        changeTitleBtn = QPushButton("Change Label")
        changeTitleBtn.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        changeTitleBtn.clicked.connect(
            partial(self.changeTitle, self.data_line_ch6, TitleBox, self.PlotGraph2))
        buttonsLayout.addWidget(changeTitleBtn, 2)

        movePlots = QPushButton("Move Plots")
        movePlots.setStyleSheet(
            "font-size:14px; background-color:#AFE1AF; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        movePlots.clicked.connect(lambda: self.moveSignal(5))
        buttonsLayout.addWidget(movePlots)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.HideCheckBoxChannel6 = QCheckBox("Hide", self)
        self.HideCheckBoxChannel6.setStyleSheet("font-size:14px;")
        buttonsLayout.addWidget(self.HideCheckBoxChannel6, 1)

        # connecting it to function
        self.HideCheckBoxChannel6.stateChanged.connect(self.hideShowSignal6)

        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))

        self.clearChannel6 = QPushButton()
        self.clearChannel6.setIcon(QIcon("images/clear.svg"))
        self.clearChannel6.setStyleSheet(
            "background: black; font-size:14px; border-radius: 6px;border: 1px solid rgba(27, 31, 35, 0.15);padding: 5px 15px;")
        self.clearChannel6.clicked.connect(partial(self.signalClear, 5))
        buttonsLayout.addWidget(self.clearChannel6, 1)
        buttonsLayout.addSpacerItem(
            QSpacerItem(100, 10, QSizePolicy.Expanding))
        chTabUI6Tab.setLayout(buttonsLayout)
        return chTabUI6Tab

    # Browse and Open the signal.
    def browse_Signal1(self):
        if self.existChannel != [1, 1, 1, 0, 0, 0]:
            self.path, self.fileExtension = QFileDialog.getOpenFileName(
                None, "Load Signal File", os.getenv('HOME'), "csv(*.csv);; text(*.txt)")
            if self.path == "":
                return

            downloadedDataChannel = [0]
            if self.fileExtension == "csv(*.csv)":
                downloadedDataChannel = pd.read_csv(self.path).iloc[:, 1]
                downloadedDataChannel = downloadedDataChannel.values.tolist()
                # sample rate
                downloadedDataChannel = downloadedDataChannel[::]

            self._addNewChannel1(downloadedDataChannel)
            self.PlayBtn.setIcon(QIcon("images/pause.ico"))
            self.PlayBtn1.setIcon(QIcon("images/pause.ico"))
            self.PlayBtn2.setIcon(QIcon("images/pause.ico"))
            self._updatePlot1()
        # else :
            # self.statusBar.showMessage("You can't add more than 3 channels, clear one of them then add again!")

    def browse_Signal2(self):
        if self.existChannel != [0, 0, 0, 1, 1, 1]:
            self.path, self.fileExtension = QFileDialog.getOpenFileName(
                None, "Load Signal File", os.getenv('HOME'), "csv(*.csv);; text(*.txt)")
            if self.path == "":
                return

            downloadedDataChannel = [0]
            if self.fileExtension == "csv(*.csv)":
                downloadedDataChannel = pd.read_csv(self.path).iloc[:, 1]
                downloadedDataChannel = downloadedDataChannel.values.tolist()
                # sample rate
                downloadedDataChannel = downloadedDataChannel[::]

            self._addNewChannel2(downloadedDataChannel)
            self.PlayBtn.setIcon(QIcon("images/pause.ico"))
            self.PlayBtn1.setIcon(QIcon("images/pause.ico"))
            self.PlayBtn2.setIcon(QIcon("images/pause.ico"))
            self._updatePlot2()
        # else :
        #     self.statusBar.showMessage("You can't add more than 3 channels, clear one of them then add again!")

    def rewindSignal1(self):
        self.time_live1 = []  # Clear live time data
        self.data_channel_live_1 = []  # Clear live data for Channel 1
        self.data_channel_live_2 = []  # Clear live data for Channel 2
        self.data_channel_live_3 = []  # Clear live data for Channel 3

        self.incrementTimeAlongSignalRun1 = 1

        self.data_line_ch1.setData(self.time_live1, self.data_channel_live_1)
        self.data_line_ch2.setData(self.time_live1, self.data_channel_live_2)
        self.data_line_ch3.setData(self.time_live1, self.data_channel_live_3)

        self.setLimits()

    def rewindSignal2(self):
        self.time_live2 = []  # Clear live time data
        self.data_channel_live_4 = []  # Clear live data for Channel 4
        self.data_channel_live_5 = []  # Clear live data for Channel 5
        self.data_channel_live_6 = []  # Clear live data for Channel 6

        self.incrementTimeAlongSignalRun2 = 1

        self.data_line_ch4.setData(self.time_live2, self.data_channel_live_4)
        self.data_line_ch5.setData(self.time_live2, self.data_channel_live_5)
        self.data_line_ch6.setData(self.time_live2, self.data_channel_live_6)
        self.setLimits()

    def rewindSignal(self):
        self.time_live1 = []  # Clear live time data
        self.time_live2 = []  # Clear live time data

        self.data_channel_live_1 = []  # Clear live data for Channel 1
        self.data_channel_live_2 = []  # Clear live data for Channel 2
        self.data_channel_live_3 = []  # Clear live data for Channel 3
        self.data_channel_live_4 = []  # Clear live data for Channel 4
        self.data_channel_live_5 = []  # Clear live data for Channel 5
        self.data_channel_live_6 = []  # Clear live data for Channel 6

        self.incrementTimeAlongSignalRun1 = 1
        self.incrementTimeAlongSignalRun2 = 1

        self.data_line_ch1.setData(self.time_live1, self.data_channel_live_1)
        self.data_line_ch2.setData(self.time_live1, self.data_channel_live_2)
        self.data_line_ch3.setData(self.time_live1, self.data_channel_live_3)
        self.data_line_ch4.setData(self.time_live2, self.data_channel_live_4)
        self.data_line_ch5.setData(self.time_live2, self.data_channel_live_5)
        self.data_line_ch6.setData(self.time_live2, self.data_channel_live_6)

        self.setLimits()
        pass

    def clearAllChannels(self):
        self.time_live1 = list()
        self.time_live2 = list()

        self.data_channel_live_1 = list()
        self.data_line_ch1.clear()
        self.data_channel_live_2 = list()
        self.data_line_ch2.clear()
        self.data_channel_live_3 = list()
        self.data_line_ch3.clear()
        self.data_channel_live_4 = list()
        self.data_line_ch4.clear()
        self.data_channel_live_5 = list()
        self.data_line_ch5.clear()
        self.data_channel_live_6 = list()
        self.data_line_ch6.clear()

    def _addNewChannel1(self, downloadedDataChannel):
        if self.existChannel[0] == 0:
            self.clearAllChannels()
            self.data_channel_live_1 = []
            self.data_line_ch1.clear()

            self.data_channel_1 = downloadedDataChannel
            self.data_channel_live_1 = list()
            self.existChannel[0] = 1

            self.tabs.addTab(self.channelTabUI1(), "Channel 1")

            # self.statusBar.showMessage("Channel 1 loaded successfully.")
        elif self.existChannel[1] == 0:
            self.clearAllChannels()
            self.data_channel_live_2 = []
            self.data_line_ch2.clear()

            self.data_channel_2 = downloadedDataChannel
            self.data_channel_live_2 = list()
            self.existChannel[1] = 1

            self.tabs.addTab(self.channelTabUI2(), "Channel 2")

            # self.statusBar.showMessage("Channel 2 loaded successfully.")

        elif self.existChannel[2] == 0:
            self.clearAllChannels()
            self.data_channel_live_3 = []
            self.data_line_ch3.clear()

            self.data_channel_3 = downloadedDataChannel
            self.data_channel_live_3 = list()
            self.existChannel[2] = 1

            self.tabs.addTab(self.channelTabUI3(), "Channel 3")

            # self.statusBar.showMessage("Channel 3 loaded successfully")

        # else :
        #     self.statusBar.showMessage("You can't add more than 3 channels, clear one of them then add again!")
        self.addZerosChannel1()

    def _addNewChannel2(self, downloadedDataChannel):
        if self.existChannel[3] == 0:
            self.clearAllChannels()
            self.data_channel_live_4 = []
            self.data_line_ch4.clear()

            self.data_channel_4 = downloadedDataChannel
            self.data_channel_live_4 = list()
            self.existChannel[3] = 1

            self.tabs.addTab(self.channelTabUI4(), "Channel 4")

            # self.statusBar.showMessage("Channel 4 loaded successfully.")

        elif self.existChannel[4] == 0:
            self.clearAllChannels()
            self.data_channel_live_5 = []
            self.data_line_ch5.clear()

            self.data_channel_5 = downloadedDataChannel
            self.data_channel_live_5 = list()
            self.existChannel[4] = 1

            self.tabs.addTab(self.channelTabUI5(), "Channel 5")

            # self.statusBar.showMessage("Channel 5 loaded successfully.")

        elif self.existChannel[5] == 0:
            self.clearAllChannels()
            self.data_channel_live_6 = []
            self.data_line_ch6.clear()

            self.data_channel_6 = downloadedDataChannel
            self.data_channel_live_6 = list()
            self.existChannel[5] = 1

            self.tabs.addTab(self.channelTabUI6(), "Channel 6")

            # self.statusBar.showMessage("Channel 6 loaded successfully.")

        # else :
        #     self.statusBar.showMessage("You can't add more than 3 channels, clear one of them then add again!")
        self.addZerosChannel2()

    def addZerosChannel1(self):
        dataLengths = [len(self.data_channel_1), len(self.data_channel_2), len(self.data_channel_3), len(
            self.data_channel_4), len(self.data_channel_5), len(self.data_channel_6)]

        maxLength = max(dataLengths)
        for _ in range(maxLength-dataLengths[0]):
            self.data_channel_1.append(np.random.randint(0, 10))
        for _ in range(maxLength-dataLengths[1]):
            self.data_channel_2.append(np.random.randint(0, 10))
        for _ in range(maxLength-dataLengths[2]):
            self.data_channel_3.append(np.random.randint(0, 10))
        self.time1 = np.linspace(0, maxLength-1, maxLength)
        self.time_live1 = list()

    def addZerosChannel2(self):
        dataLengths = [len(self.data_channel_1), len(self.data_channel_2), len(self.data_channel_3), len(
            self.data_channel_4), len(self.data_channel_5), len(self.data_channel_6)]

        maxLength = max(dataLengths)
        for _ in range(maxLength-dataLengths[3]):
            self.data_channel_4.append(np.random.randint(0, 10))
        for _ in range(maxLength-dataLengths[4]):
            self.data_channel_5.append(np.random.randint(0, 10))
        for _ in range(maxLength-dataLengths[5]):
            self.data_channel_6.append(np.random.randint(0, 10))
        self.time2 = np.linspace(0, maxLength-1, maxLength)
        self.time_live2 = list()

    # Export information in PDF
    def takeSnapshot(self):
        self.snapshotNumber += 1
        exporter1 = pyqtgraph.exporters.ImageExporter(self.GrLayout1.scene())
        exporter2 = pyqtgraph.exporters.ImageExporter(self.GrLayout2.scene())
        exporter1.export('images/image1.png')
        exporter2.export('images/image2.png')

        input_file = "others/blank.pdf"
        image_file1 = "images/image1.png"
        image_file2 = "images/image2.png"

        # Adding Image
        img1 = open(image_file1, "rb").read()
        img2 = open(image_file2, "rb").read()
        rect = fitz.Rect(100, 50, 450, 400)
        doc = fitz.open(input_file)

        page2 = doc.new_page(1)

        p = fitz.Point(100, 50)
        title = f"Snapshot {self.snapshotNumber} \nStatistics Report about plot 1:"
        title2 = "Statistics Report about plot 2:"
        doc[0].insert_text(p, title, fontsize=20)

        doc[0].insert_image(rect, stream=img1)

        page2.insert_text(p, title2, fontsize=20)
        page2.insert_image(rect, stream=img2)

        if self.existChannel[0] == 1:
            # Channel 1 information
            p = fitz.Point(100, 400)
            titleChannel1 = "Channel 1:"
            doc[0].insert_text(p, titleChannel1, fontsize=15)

            p = fitz.Point(100, 425)
            StatisticsChannel1 = self.channelStatisticsGet(
                self.data_channel_1)
            doc[0].insert_text(p, StatisticsChannel1, fontsize=12)

        if self.existChannel[1] == 1:
            # Channel 2 information
            p = fitz.Point(100, 525)
            titleChannel2 = "Channel 2:"
            doc[0].insert_text(p, titleChannel2, fontsize=15)

            p = fitz.Point(100, 550)
            StatisticsChannel2 = self.channelStatisticsGet(
                self.data_channel_2)
            doc[0].insert_text(p, StatisticsChannel2, fontsize=12)

        if self.existChannel[2] == 1:
            # Channel 3 information
            p = fitz.Point(100, 650)
            titleChannel3 = "Channel 3:"
            doc[0].insert_text(p, titleChannel3, fontsize=15)

            p = fitz.Point(100, 675)
            StatisticsChannel3 = self.channelStatisticsGet(
                self.data_channel_3)
            doc[0].insert_text(p, StatisticsChannel3, fontsize=12)

        if self.existChannel[3] == 1:
            # Channel 4 information
            p = fitz.Point(100, 400)
            titleChannel4 = "Channel 4:"
            page2.insert_text(p, titleChannel4, fontsize=15)

            p = fitz.Point(100, 425)
            StatisticsChannel4 = self.channelStatisticsGet(
                self.data_channel_4)
            page2.insert_text(p, StatisticsChannel4, fontsize=12)

        if self.existChannel[4] == 1:
            # Channel 5 information
            p = fitz.Point(100, 525)
            titleChannel5 = "Channel 5:"
            page2.insert_text(p, titleChannel5, fontsize=15)

            p = fitz.Point(100, 550)
            StatisticsChannel5 = self.channelStatisticsGet(
                self.data_channel_5)
            page2.insert_text(p, StatisticsChannel5, fontsize=12)

        if self.existChannel[5] == 1:
            # Channel 6 information
            p = fitz.Point(100, 650)
            titleChannel6 = "Channel 6:"
            page2.insert_text(p, titleChannel6, fontsize=15)

            p = fitz.Point(100, 675)
            StatisticsChannel6 = self.channelStatisticsGet(
                self.data_channel_6)
            page2.insert_text(p, StatisticsChannel6, fontsize=12)

        self.snapshots.append(doc)

    def exportPDF(self):
        input_file = "others/blank.pdf"
        output_file, _ = QFileDialog.getSaveFileName(
            self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')

        if output_file != '':
            if QFileInfo(output_file).suffix() == "":
                output_file += '.pdf'

            # Create a new document to store all pages
            combined_doc = fitz.open(input_file)

            # Iterate over self.snapshots and append pages to the new document
            for snapshot_doc in self.snapshots:
                for i in range(len(snapshot_doc)):
                    combined_doc.insert_pdf(
                        snapshot_doc, from_page=i, to_page=i)

            combined_doc.delete_page(0)
            # Save the combined document
            combined_doc.save(output_file)
            combined_doc.close()

    def channelStatisticsGet(self, data_channel):
        meanChannel = "Mean: " + \
            str("{:.2f}".format(np.mean(data_channel))) + "\n"
        stdChannel = "Std: " + \
            str("{:.2f}".format(np.std(data_channel))) + "\n"
        minValueChannel = "Minimum: " + \
            str("{:.2f}".format(min(data_channel))) + "\n"
        maxValueChannel = "Maximum: " + \
            str("{:.2f}".format(max(data_channel))) + "\n"

        StatisticsChannel = meanChannel + stdChannel + minValueChannel + maxValueChannel

        return StatisticsChannel

    # Change Color of Channel
    def changeColorBtn(self, data_line, colorbtn):
        def done(btn):
            data_line.setPen(btn.color())

        colorbtn.sigColorChanged.connect(done)

    # Show and Hide the signal

    def hideShowSignal1(self):
        if self.HideCheckBoxChannel1.isChecked():
            # self.statusBar.showMessage("Channel 1 is hided")
            self.data_line_ch1.hide()
        else:
            # self.statusBar.showMessage("Channel 1 is showed")
            self.data_line_ch1.show()

    def hideShowSignal2(self):
        if self.HideCheckBoxChannel2.isChecked():
            # self.statusBar.showMessage("Channel 2 is hided")
            self.data_line_ch2.hide()
        else:
            # self.statusBar.showMessage("Channel 2 is showed")
            self.data_line_ch2.show()

    def hideShowSignal3(self):
        if self.HideCheckBoxChannel3.isChecked():
            # self.statusBar.showMessage("Channel 3 is hided")
            self.data_line_ch3.hide()
        else:
            # self.statusBar.showMessage("Channel 3 is showed")
            self.data_line_ch3.show()

    def hideShowSignal4(self):
        if self.HideCheckBoxChannel4.isChecked():
            # self.statusBar.showMessage("Channel 4 is hided")
            self.data_line_ch4.hide()
        else:
            # self.statusBar.showMessage("Channel 4 is showed")
            self.data_line_ch4.show()

    def hideShowSignal5(self):
        if self.HideCheckBoxChannel5.isChecked():
            # self.statusBar.showMessage("Channel 5 is hided")
            self.data_line_ch5.hide()
        else:
            # self.statusBar.showMessage("Channel 5 is showed")
            self.data_line_ch5.show()

    def hideShowSignal6(self):
        if self.HideCheckBoxChannel6.isChecked():
            # self.statusBar.showMessage("Channel 6 is hided")
            self.data_line_ch6.hide()
        else:
            # self.statusBar.showMessage("Channel 6 is showed")
            self.data_line_ch6.show()

    # Change title of the signal
    def changeTitle(self, data_line, TitleBox, plot):
        if plot == self.PlotGraph1:
            self.legendItemName1.removeItem(data_line)
            self.legendItemName1.addItem(data_line, TitleBox.text())
        else:
            self.legendItemName2.removeItem(data_line)
            self.legendItemName2.addItem(data_line, TitleBox.text())

    # set Limits of signal
    def setLimits(self):
        pass

    def move(self):
        # self.data_line_ch4.setData(self.time_live1, self.data_channel_live_1)
        self.update_view_range(self.PlotGraph2, self.time_live1)

    def moveSignal(self, channel_index):
        # Check if the channel exists in Plot 1
        if self.existChannel[channel_index] == 1:
            # Copy the data from Plot 1 to Plot 2 for the selected channel
            self.timer0 = QTimer()
            self.timer0.setInterval(int(1*(100-self.speed)))
            self.timer0.start()
            if channel_index == 0:
                if self.existChannel[3] == 0:
                    self.data_line_ch1 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_4, name="Moved Ch 4", pen="g")
                    self.timer0.timeout.connect(self.move)
                elif self.existChannel[3] == 1 and self.existChannel[4] == 0:
                    self.data_line_ch1 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_5, name="Moved Ch 5", pen="purple")
                    self.timer0.timeout.connect(self.move)
                elif self.existChannel[4] == 1 and self.existChannel[5] == 0:
                    self.data_line_ch1 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_6, name="Moved Ch 6", pen=(173, 216, 230))
                    self.timer0.timeout.connect(self.move)
            elif channel_index == 1:
                if self.existChannel[3] == 0:
                    self.data_line_ch2 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_4, name="Moved Ch 4", pen="g")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[3] == 1 and self.existChannel[4] == 0:
                    self.data_line_ch2 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_5, name="Moved Ch 5", pen="purple")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[4] == 1 and self.existChannel[5] == 0:
                    self.data_line_ch2 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_6, name="Moved Ch 6", pen=(173, 216, 230))
                    self.timer0.timeout.connect(self.move)
            elif channel_index == 2:
                if self.existChannel[3] == 0:
                    self.data_line_ch3 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_4, name="Moved Ch 4", pen="g")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[3] == 1 and self.existChannel[4] == 0:
                    self.data_line_ch3 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_5, name="Moved Ch 5", pen="purple")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[4] == 1 and self.existChannel[5] == 0:
                    self.data_line_ch3 = self.PlotGraph2.plot(
                        self.time_live2, self.data_channel_live_6, name="Moved Ch 6", pen=(173, 216, 230))
                    self.timer0.timeout.connect(self.move)
            if channel_index == 3:
                if self.existChannel[0] == 0:
                    self.data_line_ch4 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_1, name="Moved Ch 1", pen="g")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[0] == 1 and self.existChannel[1] == 0:
                    self.data_line_ch4 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_2, name="Moved Ch 2", pen="purple")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[1] == 1 and self.existChannel[2] == 0:
                    self.data_line_ch4 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_3, name="Moved Ch 3", pen=(173, 216, 230))
                    self.timer0.timeout.connect(self.move)
            elif channel_index == 4:
                if self.existChannel[0] == 0:
                    self.data_line_ch5 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_1, name="Moved Ch 1", pen="g")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[0] == 1 and self.existChannel[1] == 0:
                    self.data_line_ch5 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_2, name="Moved Ch 2", pen="purple")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[1] == 1 and self.existChannel[2] == 0:
                    self.data_line_ch5 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_3, name="Moved Ch 3", pen=(173, 216, 230))
                    self.timer0.timeout.connect(self.move)
            elif channel_index == 5:
                if self.existChannel[0] == 0:
                    self.data_line_ch6 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_1, name="Moved Ch 1", pen="g")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[0] == 1 and self.existChannel[1] == 0:
                    self.data_line_ch6 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_2, name="Moved Ch 2", pen="purple")
                    self.timer0.timeout.connect(self.move)
                if self.existChannel[1] == 1 and self.existChannel[2] == 0:
                    self.data_line_ch6 = self.PlotGraph1.plot(
                        self.time_live1, self.data_channel_live_3, name="Moved Ch 3", pen=(173, 216, 230))
                    self.timer0.timeout.connect(self.move)
            # Clear the data from Plot 1 for the selected channel

    def signalClear(self, channelNumber):
        if channelNumber == 0:
            self.data_line_ch1.clear()
            self.data_channel_1 = [0]
            self.data_channel_live_1 = [0]
            self.tabs.removeTab(1)
        elif channelNumber == 1:
            self.data_line_ch2.clear()
            self.data_channel_2 = [0]
            self.data_channel_live_2 = [0]
            self.tabs.removeTab(2)
        elif channelNumber == 2:
            self.data_line_ch3.clear()
            self.data_channel_3 = [0]
            self.data_channel_live_3 = [0]
            self.tabs.removeTab(3)
        elif channelNumber == 3:
            self.data_line_ch4.clear()
            self.data_channel_4 = [0]
            self.data_channel_live_4 = [0]
            self.tabs.removeTab(4)
        elif channelNumber == 4:
            self.data_line_ch5.clear()
            self.data_channel_5 = [0]
            self.data_channel_live_5 = [0]
            self.tabs.removeTab(5)
        elif channelNumber == 5:
            self.data_line_ch6.clear()
            self.data_channel_6 = [0]
            self.data_channel_live_6 = [0]
            self.tabs.removeTab(6)

        self.PlayBtn.setIcon(QIcon("images/pause.ico"))
        self.existChannel[channelNumber] = 0
        self._updatePlot1()
        self._updatePlot2()

    # Quit the window

    def exit(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Exit the application")
        dlg.setText("Are you sure you want to exit the application ?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec()

        if button == QMessageBox.Yes:
            sys.exit()


if __name__ == "__main__":
    # Initialize Our Window App
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = Window()
    win.show()

    # Run the application
    sys.exit(app.exec_())
