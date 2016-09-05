class ListStyle():
	@staticmethod
	def list(select, request):
		list_of_dicts = []
		
		page = request.args.get('page')
		number = request.args.get('number')

		try:
			page = int(page) if page else 1
		except:
			page = 1
		try:
			number = int(number) if number else 10
		except:
			number = 10 
		paging = {}
		paging['prev'] = None if page == 1 else (page - 1)
		
		calc = select.count() // number + (select.count() % number > 0)
		
		paging['next'] = None if page >= calc else page + 1
		# if page >= calc:
		# 	paging['next'] = None
		# else:
		# 	paging['next'] = page + 1

		if paging['prev'] != None:
			paging['prev'] = "%s%s%d%s%d" % (request.base_url, "?page=", paging['prev'], "&number=", number)

		if paging['next'] != None:
			paging['next'] = "%s%s%d%s%d" % (request.base_url, "?page=", paging['next'], "&number=", number)

		select = select.paginate(page, number)
		for obj in select:
			list_of_dicts.append(obj.to_dict())
		return {
			'data': list_of_dicts,
			'paging': paging
		}
