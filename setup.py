from distutils.core import setup

setup(
    name='picka',
    version="0.7.9",
    description="picka generates randomized, realistic data for use in any application.",
    author="Anthony Long",
    author_email="antlong@gmail.com",
    packages=["picka"],
    include_package_data=True,
    package_data={'picka': ['*.sqlite', '*.txt', '*.json', ], },
    install_requires=['jsonlib'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python', ],
    zip_safe=False,
)
