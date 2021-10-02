if __name__ == '__main__':

    import json
    import io
    import sys

    try:
        if sys.argv[1].lower() == 's' or 'sale':
            in_file = 'sale.json'
            out_file = 'sale_final.json'
    except IndexError:
        in_file = 'lease.json'
        out_file = 'lease_final.json'

    with io.open(in_file, encoding='utf-8') as f:
        data = json.load(f)
    f.close()

    params = {'Балкон': 'balcony',
              'Ремонт': 'renovation',
              'Год постройки': 'year_built',
              'Газ': 'gas',
              'Высота потолков': 'ceiling',
              'Лифт': 'elevator',
              'Коммуникации': 'communication',
              'Охрана': 'security',
              'Материал стен': 'walls',
              'Стороны света': 'side'}

    for row in data:
        row['floor'] = int(row['floor'])
        row['area'] = int(row['area'])
        row['city'] = row['address'].split()[0][:-1]
        row['address'] = ' '.join(row['address'].split()[1:])

        try:
            for x in row['params']:
                try:
                    k, v = x.split(':', 1)
                    row[params[k]] = v[1:]
                except ValueError:
                    row['mortgage'] = 'yes'
            del row['params']
        except KeyError:
            pass


        try:
            del row['photo_inside']
            del row['photo_outside']
        except KeyError:
            pass

    with io.open(out_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2, sort_keys=True)