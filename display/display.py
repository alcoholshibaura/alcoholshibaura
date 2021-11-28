#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file display.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import cv2
import pygame.mixer
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
display_spec = ["implementation_id", "display",
		 "type_name",         "display",
		 "description",       "ModuleDescription",
		 "version",           "1.0.0",
		 "vendor",            "VenderName",
		 "category",          "Animation",
		 "activity_type",     "STATIC",
		 "max_instance",      "1",
		 "language",          "Python",
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class display
# @brief ModuleDescription
#
#
class display(OpenRTM_aist.DataFlowComponentBase):

	##
	# @brief constructor
	# @param manager Maneger Object
	#
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_content = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
		"""
		"""
		self._contentIn = OpenRTM_aist.InPort("content", self._d_content)





		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">

		# </rtc-template>



	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry()
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onInitialize(self):
		# Bind variables and configuration variable

		# Set InPort buffers
		self.addInPort("content",self._contentIn)

		# Set OutPort buffers

		# Set service provider to Ports

		# Set service consumers to Ports

		# Set CORBA Service Ports

		return RTC.RTC_OK

	###
	##
	## The finalize action (on ALIVE->END transition)
	## formaer rtc_exiting_entry()
	##
	## @return RTC::ReturnCode_t
	#
	##
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK

	###
	##
	## The startup action when ExecutionContext startup
	## former rtc_starting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The shutdown action when ExecutionContext stop
	## former rtc_stopping_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK

	##
	#
	# The activated action (Active state entry action)
	# former rtc_active_entry()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onActivated(self, ec_id):
		print("Acitvated")
		return RTC.RTC_OK

	##
	#
	# The deactivated action (Active state exit action)
	# former rtc_active_exit()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onDeactivated(self, ec_id):
		print("Deactivated")
		return RTC.RTC_OK

	##
	#
	# The execution action that is invoked periodically
	# former rtc_active_do()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#
	def onExecute(self, ec_id):
		#入力ポートからデータを取得したときの処理
		if self._contentIn.isNew():
			self._d_content = self._contentIn.read()
			content_new= self._d_content.data
			print(content_new)

			#前回取得したデータの取得
			f = open('/home/pi/alcohol/display/content_old.txt', 'r', encoding = 'UTF-8')
			content_old= int(f.read())

			#手がハンドドライヤー内に入ったときの処理
			if content_new == 1:

				cap = cv2.VideoCapture(r'/home/pi/alcohol/display/movie.mp4')

				if (cap.isOpened() == False):
					print("ビデオファイルを開くとエラーが発生しました")

				while (cap.isOpened()):

					ret, frame = cap.read()
					if ret == True:

						cv2.imshow('Video', frame)

						if cv2.waitKey(1) & 0xFF == ord('q'):
							break
					else :
						break

				cap.release()

				cv2.destroyAllWindows()

			#人が侵入したときの処理
			if content_old != 2 and content_new == 2:
				pygame.mixer.init(frequency = 25000)
				pygame.mixer.music.load('/home/pi/alcohol/display/speaker.mp3')
				pygame.mixer.music.play(1)
				time.sleep(3)
				pygame.mixer.music.stop()
			f.close()

			#今回取得したデータの保存
			f = open('/home/pi/alcohol/display/content_old.txt', 'w', encoding = 'UTF-8')
			f.write(str(content_new))
			f.close()


		return RTC.RTC_OK

	###
	##
	## The aborting action when main logic error occurred.
	## former rtc_aborting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The error action in ERROR state
	## former rtc_error_do()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The reset action that is invoked resetting
	## This is same but different the former rtc_init_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The state update action that is invoked after onExecute() action
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##

	##
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK

	###
	##
	## The action that is invoked when execution context's rate is changed
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK




def displayInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=display_spec)
    manager.registerFactory(profile,
                            display,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    displayInit(manager)

    # Create a component
    comp = manager.createComponent("display")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

