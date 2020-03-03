# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re


class AllRecipes(object):

	@staticmethod
	def search(query_dict):
		"""
		Search recipes parsing the returned html data.
		"""
		base_url = "https://allrecipes.com/search/results/?"
		query_url = urllib.parse.urlencode(query_dict)

		url = base_url + query_url

		req = urllib.request.Request(url)
		req.add_header('Cookie', 'euConsent=true')

		html_content = urllib.request.urlopen(req).read()

		soup = BeautifulSoup(html_content, 'html.parser')

		search_data = []
		articles = soup.findAll("article", {"class": "fixed-recipe-card"})

		iterarticles = iter(articles)
		next(iterarticles)
		for article in iterarticles:
			data = {}
			try:
				data["name"] = article.find("h3", {"class": "fixed-recipe-card__h3"}).get_text().strip(' \t\n\r')
				data["description"] = article.find("div", {"class": "fixed-recipe-card__description"}).get_text().strip(
					' \t\n\r')
				data["url"] = article.find("a", href=re.compile('^https://www.allrecipes.com/recipe/'))['href']
				try:
					data["image"] = \
					article.find("a", href=re.compile('^https://www.allrecipes.com/recipe/')).find("img")[
						"data-original-src"]
				except Exception as e1:
					pass
				try:
					data["rating"] = float(
						article.find("div", {"class": "component recipe-ratings"}).find("span")["review-star-text"])
				except ValueError:
					data["rating"] = None
			except Exception as e2:
				pass
			if data and "image" in data:  # Do not include if no image -> its probably an add or something you do not want in your result
				search_data.append(data)

		return search_data

	@staticmethod
	def get(url):
		"""
		'url' from 'search' method.
		 ex. "/recipe/106349/beef-and-spinach-curry/"
		"""
		# base_url = "https://allrecipes.com/"
		# url = base_url + uri
		str1 = 'prep'

		req = urllib.request.Request(url)
		req.add_header('Cookie', 'euConsent=true')

		html_content = urllib.request.urlopen(req).read()
		soup = BeautifulSoup(html_content, 'html.parser')

		try:
			rating = (soup.find("div", {"class": "component recipe-ratings"}))
			rating = rating.find("span", {"class": "review-star-text"}).get_text()
			rating = float(''.join(re.findall(r'\d.', rating)))
		except:

			rating = soup.find(itemprop="ratingValue").get("content")
		# rating= rating.find("meta").get_text()
		# rating= rating.find("")
		# rating = None

		try:
			name = soup.find("h1", {"class": "headline heading-content"}).get_text().replace("®", "")
		except:
			name = soup.find("h1", {"itemprop": "name"}).get_text()
		# name= name.find("itemprop", {"name"}).get_text()

		data = {
			"rating": rating,
			"ingredients": [],
			"steps": [],
			"name": name,
			"prep_time_and_servings": [],
			"nutrients": []
		}


		ingredients = soup.findAll('span', attrs={'itemprop': "recipeIngredient"})
		if len(ingredients) != 0:
			for ingred in ingredients:
				ingred = ingred.get_text().rstrip()

				#			if str_ing and str_ing != "Add all ingredients to list":
				data["ingredients"].append(ingred.rstrip())
		else:
			ingredients = soup.findAll("li", {"class": "ingredients-item"})
			for ingredient in ingredients:
				str_ing = ingredient.find("span", {"class": "ingredients-item-name"}).get_text().rstrip()
				if str_ing and str_ing != "Add all ingredients to list":
					data["ingredients"].append(str_ing.rstrip())
		# print(ingredien)

		steps = soup.findAll("li", {"class": "subcontainer instructions-section-item"})
		if len(steps) !=0:
			for step in steps:
				str_step = step.find("div", {"class": "section-body"}).get_text()
				if str_step:
					data["steps"].append(str_step)

		else:
			steps= soup.findAll("li", {"class": "step"})
			for step in steps:
				step= step.find("span", {"recipe-directions__list--item"}).get_text().rstrip()
				if step:
					data["steps"].append(step.rstrip())

		nutrition_data = soup.findAll("div", {"class": "nutrition-row"})

		if len(nutrition_data) !=0:
			for nutrient in nutrition_data:
				nut = nutrient.find("span", {"class": "nutrient-name"}).get_text().rstrip()
				# amount = nutrient.find("span", {"class": "nutrient-value"}).get_text().strip()
				if nut:
					data['nutrients'].append(nut.rstrip())

		else:
			#nutrition_data = soup.findAll("div", {"class": "nutrition-summary-facts"})
			calories= soup.find(itemprop = "calories").get_text().strip(';') + ','
			fat = soup.find(itemprop="fatContent").get_text().strip() + 'g fat,'
			carbs = soup.find(itemprop="carbohydrateContent").get_text().strip() + 'g carbohydrates,'
			protein = soup.find(itemprop="proteinContent").get_text().strip()  + 'g protein,'
			cholesterol  = soup.find(itemprop="cholesterolContent").get_text().strip() + 'g cholesterol,'
			sodium = soup.find(itemprop="sodiumContent").get_text().strip() + 'g sodium'
			#for nutrient in nutrition_data:
			#	nut = nutrient.find("span", {"class": "nutrient-name"}).get_text().rstrip()
				# amount = nutrient.find("span", {"class": "nutrient-value"}).get_text().strip()
			#	if nut:
			data['nutrients'].append(calories + ' ' + fat + ' ' + carbs + ' '+ protein + ' '+ cholesterol + ' ' + sodium)


		#direction_data = soup.findAll("div", {"class": "recipe-meta-item"})

		"""if len(direction_data) !=0:
			for pre in direction_data:
				# pre = pre.find("div", {"class": "recipe-meta-item"})
				prep = pre.find("div", {"class": "recipe-meta-item-header"}).get_text().strip()
				# print(prep)
				time = pre.find("div", {"class": "recipe-meta-item-body"}).get_text().strip()
				if pre:
					# print(pre)
					data["prep_time_and_servings"].append(prep + ' ' + str(time).strip())

		else:
			temp = []
			direction_data= soup.findAll("span", {"class": "prepTime__item--time"})
			#print(direction_data)

			for dir in direction_data:
				dir = dir.get_text()
				temp.append(dir)

			data["prep_time_and_servings"].append('prep' + temp[0] + ' mins',' ' + temp[1].strip())
				#print(dir)"""

		# prep_time = soup.find("div", {"class": "recipe-meta-item-body"}).get_text()
		# prep_time = str1 + ' ' + prep_time.strip()
		# cook_time = direction_data.find("time", {"itemprop": "cookTime"}).get_text()
		# total_time = direction_data.find("time", {"itemprop": "totalTime"}).get_text()

		# print(direction_data)







		return data
