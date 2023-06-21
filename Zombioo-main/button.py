import pygame 


#button class
class Button():
	#初始化按钮对象，接受参数包括按钮的初始位置(x, y)、按钮的图像image和缩放比例scale。在初始化过程中，将图像按照缩放比例进行缩放，并设置按钮的矩形边界。
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	#绘制按钮，并检测鼠标交互操作。该方法接受一个surface参数，表示将按钮绘制在哪个画布上。在绘制过程中，首先获取鼠标的位置，并检查鼠标是否在按钮的矩形边界内。如果鼠标在按钮内，并且鼠标左键被按下且按钮之前没有被点击过，则返回True，表示按钮被点击。在绘制按钮时，使用blit方法将按钮的图像绘制在指定位置上。
	def draw(self, surface):
		action = False

		#get mouse position获取鼠标位置
		pos = pygame.mouse.get_pos()

		#check mouseover获取鼠标位置
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#drawing button绘图按钮
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
        
        