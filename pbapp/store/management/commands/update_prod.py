from ...models import ProductsNutriTypeA
from ...request_.offs_req import AllRequests
from django.shortcuts import get_object_or_404, get_list_or_404


def update_db():
    products = ProductsNutriTypeA.objects.all()
    req = AllRequests()
    c = 0
    for item in products:
        try:
            productr = req.code_request(item.code)
            productj = productr.json()
            if 'product' in productj:
                print(c)
                filtProduct = productj['product']

            product_name = filtProduct['product_name']
            picture = filtProduct['image_front_url']
            category = filtProduct['pnns_groups_2']
            if item.product_name != product_name:
                change = get_object_or_404(ProductsNutriTypeA, code=item.code)
                #change.product_name = product_name
                #change.save()
                print(f'{product_name} changé à la place de {item.product_name}')
            if item.picture != picture:
                change = get_object_or_404(ProductsNutriTypeA, code=item.code)
                #change.picture = picture
                #change.save()
                print(f'{picture} changé à la place de {item.picture}')
            if item.category != category:
                change = get_object_or_404(ProductsNutriTypeA, code=item.code)
                #change.category = category
                #change.save()
                print(f'{category} changé à la place de {item.category}')
        except KeyError:
            filtProduct = productj['products']
