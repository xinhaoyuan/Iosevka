.PHONY: archive fonts clean

archive: fonts
	cd dist; tar zcvf iosevka-xy-`date +%Y%m%d`.tgz `../xy-build-plans.py --mode=print-font-ids`

fonts: private-build-plans.toml
	npm run build -- `./xy-build-plans.py --mode=print-build-targets`

clean:
	rm -rf dist

private-build-plans.toml: xy-build-plans.py
	./xy-build-plans.py --mode=generate-build-plans
